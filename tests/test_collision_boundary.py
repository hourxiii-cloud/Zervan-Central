from __future__ import annotations

import copy
import random
import unittest

from tools.collision_boundary import (
    CLEAN,
    COLLISION,
    UNRESOLVED_CONTEXT,
    AUTHORITY_STATE,
    HUMAN_GATE_STATE,
    analyze_collision_boundary,
    measurable_body_identity,
)


SURFACE = (
    "proto",
    "service",
    "src_port",
    "dst_port",
    "duration",
    "packets",
    "bytes",
)


def row(
    ref,
    label,
    *,
    proto="udp",
    service="dns",
    src_port=5353,
    dst_port=5353,
    duration=0,
    packets=1,
    bytes_=45,
):
    return {
        "member_reference": ref,
        "reviewed_label": label,
        "proto": proto,
        "service": service,
        "src_port": src_port,
        "dst_port": dst_port,
        "duration": duration,
        "packets": packets,
        "bytes": bytes_,
        "provenance_reference": "fixture:rt-iot2022",
    }


def repeated_group(
    prefix,
    count,
    labels,
    **body,
):
    records = []

    for index in range(count):
        records.append(
            row(
                f"{prefix}:{index:03d}",
                labels[index % len(labels)],
                **body,
            )
        )

    return records


def rt_iot2022_fixture():
    rows = []

    # 75 — Thing_Speak / ARP / Slowloris
    rows += repeated_group(
        "fb_c7f399460f4e5520",
        75,
        ("Thing_Speak", "ARP", "Slowloris"),
        proto="udp",
        service="dns",
        src_port=5353,
        dst_port=5353,
        bytes_=45,
    )

    # 24 — ARP / Thing_Speak
    rows += repeated_group(
        "fb_eae67d977ad4ef9e",
        24,
        ("ARP", "Thing_Speak"),
        proto="udp",
        service="dns",
        src_port=5353,
        dst_port=5353,
        bytes_=115,
    )

    # 17 — ARP / NMAP UDP
    rows += repeated_group(
        "fb_4d660163c98d6626",
        17,
        ("ARP", "NMAP_UDP"),
        proto="udp",
        service="dhcp",
        src_port=68,
        dst_port=67,
        bytes_=548,
    )

    # 4 — ARP / Thing_Speak — ICMP
    rows += repeated_group(
        "fb_2a8c56513677a96d",
        4,
        ("ARP", "Thing_Speak"),
        proto="icmp",
        service="-",
        src_port=135,
        dst_port=136,
        bytes_=24,
    )

    # 4 — ARP / Thing_Speak — DHCP
    rows += repeated_group(
        "fb_b688ba219c2e43ac",
        4,
        ("ARP", "Thing_Speak"),
        proto="udp",
        service="dhcp",
        src_port=68,
        dst_port=67,
        bytes_=300,
    )

    # 4 — Metasploit / NMAP UDP — mDNS/DNS 5353 seam
    rows += repeated_group(
        "fb_7203e33499ec09b0",
        4,
        ("Metasploit", "NMAP_UDP"),
        proto="udp",
        service="dns",
        src_port=5353,
        dst_port=5353,
        bytes_=139,
    )

    return rows


class CollisionBoundaryTests(unittest.TestCase):

    def test_same_body_same_label_clean(self):
        rows = [
            row("a", "ARP"),
            row("b", "ARP"),
        ]

        result = analyze_collision_boundary(
            rows,
            SURFACE,
        )

        self.assertEqual(result.clean_rows, 2)
        self.assertEqual(result.collision_rows, 0)
        self.assertEqual(len(result.collision_groups), 0)

    def test_same_body_different_labels_collision(self):
        rows = [
            row("a", "ARP"),
            row("b", "Thing_Speak"),
        ]

        result = analyze_collision_boundary(
            rows,
            SURFACE,
        )

        self.assertEqual(result.clean_rows, 0)
        self.assertEqual(result.collision_rows, 2)
        self.assertEqual(len(result.collision_groups), 1)

    def test_three_labels_one_collision_group(self):
        rows = [
            row("a", "ARP"),
            row("b", "Thing_Speak"),
            row("c", "Slowloris"),
        ]

        result = analyze_collision_boundary(
            rows,
            SURFACE,
        )

        self.assertEqual(len(result.collision_groups), 1)

        self.assertEqual(
            result.collision_groups[0].distinct_labels,
            ("ARP", "Slowloris", "Thing_Speak"),
        )

    def test_body_identity_deterministic(self):
        record = row("a", "ARP")

        first = measurable_body_identity(
            record,
            SURFACE,
        )

        second = measurable_body_identity(
            copy.deepcopy(record),
            tuple(reversed(SURFACE)),
        )

        self.assertEqual(first, second)
        self.assertTrue(first.startswith("sha512:"))
        self.assertEqual(len(first), 135)

    def test_label_excluded_from_body_identity(self):
        first = row("a", "ARP")
        second = row("b", "Slowloris")

        self.assertEqual(
            measurable_body_identity(first, SURFACE),
            measurable_body_identity(second, SURFACE),
        )

    def test_label_cannot_enter_surface(self):
        with self.assertRaises(ValueError):
            measurable_body_identity(
                row("a", "ARP"),
                SURFACE + ("reviewed_label",),
            )

    def test_member_reference_cannot_enter_surface(self):
        with self.assertRaises(ValueError):
            measurable_body_identity(
                row("a", "ARP"),
                SURFACE + ("member_reference",),
            )

    def test_different_body_not_collision(self):
        rows = [
            row("a", "ARP", bytes_=45),
            row("b", "ARP", bytes_=46),
        ]

        result = analyze_collision_boundary(
            rows,
            SURFACE,
        )

        self.assertEqual(result.clean_rows, 2)
        self.assertEqual(result.collision_rows, 0)

    def test_reordering_preserves_collision_identity(self):
        rows = [
            row("a", "ARP"),
            row("b", "Thing_Speak"),
            row("c", "Slowloris"),
        ]

        first = analyze_collision_boundary(
            rows,
            SURFACE,
        )

        shuffled = list(rows)
        random.Random(41).shuffle(shuffled)

        second = analyze_collision_boundary(
            shuffled,
            SURFACE,
        )

        self.assertEqual(
            first.collision_groups[0].collision_group_id,
            second.collision_groups[0].collision_group_id,
        )

        self.assertEqual(
            first.collision_groups[0].measurable_body_sha512,
            second.collision_groups[0].measurable_body_sha512,
        )

    def test_missing_measurable_field_unresolved(self):
        record = row("a", "ARP")
        del record["bytes"]

        result = analyze_collision_boundary(
            [record],
            SURFACE,
        )

        self.assertEqual(result.clean_rows, 0)
        self.assertEqual(result.collision_rows, 0)
        self.assertEqual(result.unresolved_context_rows, 1)

        self.assertEqual(
            result.row_dispositions[0][
                "population_disposition"
            ],
            UNRESOLVED_CONTEXT,
        )

    def test_collision_not_in_supervised_population(self):
        rows = [
            row("collision:a", "ARP"),
            row("collision:b", "Thing_Speak"),
            row(
                "clean:a",
                "Benign",
                bytes_=999,
            ),
        ]

        result = analyze_collision_boundary(
            rows,
            SURFACE,
        )

        supervised = set(
            result.supervised_member_references()
        )

        self.assertEqual(supervised, {"clean:a"})
        self.assertNotIn("collision:a", supervised)
        self.assertNotIn("collision:b", supervised)

    def test_counts_reconcile(self):
        rows = [
            row("collision:a", "ARP"),
            row("collision:b", "Thing_Speak"),
            row("clean:a", "Benign", bytes_=999),
        ]

        unresolved = row(
            "unresolved:a",
            "Unknown",
            bytes_=500,
        )
        del unresolved["service"]
        rows.append(unresolved)

        result = analyze_collision_boundary(
            rows,
            SURFACE,
        )

        self.assertTrue(result.reconcile())

        self.assertEqual(
            result.total_source_rows,
            result.clean_rows
            + result.collision_rows
            + result.unresolved_context_rows,
        )

    def test_rt_iot2022_fixture_totals(self):
        result = analyze_collision_boundary(
            rt_iot2022_fixture(),
            SURFACE,
        )

        self.assertEqual(
            result.total_source_rows,
            128,
        )
        self.assertEqual(
            result.collision_rows,
            128,
        )
        self.assertEqual(
            result.clean_rows,
            0,
        )
        self.assertEqual(
            result.unresolved_context_rows,
            0,
        )
        self.assertEqual(
            len(result.collision_groups),
            6,
        )

    def test_rt_iot2022_group_sizes(self):
        result = analyze_collision_boundary(
            rt_iot2022_fixture(),
            SURFACE,
        )

        sizes = sorted(
            (
                group.member_count
                for group in result.collision_groups
            ),
            reverse=True,
        )

        self.assertEqual(
            sizes,
            [75, 24, 17, 4, 4, 4],
        )

    def test_rt_iot2022_lane_counts(self):
        rows = rt_iot2022_fixture()

        dns_5353 = sum(
            record["proto"] == "udp"
            and record["src_port"] == 5353
            and record["dst_port"] == 5353
            for record in rows
        )

        dhcp = sum(
            record["proto"] == "udp"
            and record["src_port"] == 68
            and record["dst_port"] == 67
            for record in rows
        )

        icmp = sum(
            record["proto"] == "icmp"
            for record in rows
        )

        self.assertEqual(dns_5353, 103)
        self.assertEqual(dhcp, 21)
        self.assertEqual(icmp, 4)

    def test_metasploit_nmap_udp_seam_preserved(self):
        result = analyze_collision_boundary(
            rt_iot2022_fixture(),
            SURFACE,
        )

        seam = [
            group
            for group in result.collision_groups
            if set(group.distinct_labels)
            == {"Metasploit", "NMAP_UDP"}
        ]

        self.assertEqual(len(seam), 1)
        self.assertEqual(seam[0].member_count, 4)

    def test_collision_distinct_from_anomaly(self):
        result = analyze_collision_boundary(
            [
                row("a", "ARP"),
                row("b", "Thing_Speak"),
            ],
            SURFACE,
        )

        for record in result.row_dispositions:
            self.assertEqual(
                record["population_disposition"],
                COLLISION,
            )
            self.assertNotIn(
                "anomaly",
                record,
            )

    def test_authority_boundary(self):
        self.assertEqual(
            AUTHORITY_STATE,
            "NONE",
        )
        self.assertEqual(
            HUMAN_GATE_STATE,
            "ACTIVE",
        )


if __name__ == "__main__":
    unittest.main()
