from __future__ import annotations

import json
import tempfile
import threading
import unittest
from pathlib import Path

from candidate.v40.runtime.transition_writer import (
    TransitionWitnessWriter,
    event_digest,
)


CONTRACT_REF = "OC-AC-09"
CONTRACT_INSTANCE_ID = "OCI-AC-09-ATOMIC"
ROUTE_LOCK = "ac09.atomic.canonical.state.mutation"


def payload(index: int) -> dict:
    return {
        "event_class": "ACTIVATION",
        "from_state": "INITIALIZING",
        "to_state": "ACTIVE",
        "trigger": f"ac09-concurrency-{index}",
        "action": "state.transition",
        "request_ref": f"request:ac09:{index}",
        "reason": f"AC-09 concurrent mutation fixture {index}",
        "authorization": "CONTRACT_PERMITTED",
        "participants": [f"writer:{index}"],
        "evidence_refs": [f"evidence:ac09:{index}"],
        "conformance_before": "CONFORMING",
        "conformance_after": "CONFORMING",
        "audit_result": "PASS",
        "human_gate_latched": True,
        "decision_ref": f"decision:ac09:{index}",
        "stop_class": None,
        "scar_required": False,
        "scar_reason": None,
    }


class AC09AtomicCanonicalStateMutationTests(unittest.TestCase):

    def make_writer(
        self,
        ledger: Path,
    ) -> TransitionWitnessWriter:
        return TransitionWitnessWriter(
            ledger,
            CONTRACT_REF,
            CONTRACT_INSTANCE_ID,
            ROUTE_LOCK,
        )

    def test_independent_writers_serialize_one_canonical_chain(
        self,
    ):
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "transitions"

            writer_count = 8
            barrier = threading.Barrier(writer_count)

            results = []
            failures = []
            result_lock = threading.Lock()

            def worker(index: int) -> None:
                try:
                    writer = self.make_writer(ledger)

                    # All independent writer instances observe the ledger
                    # before being released into the append race.
                    barrier.wait(timeout=10)

                    event = writer.append(
                        payload(index)
                    )

                    with result_lock:
                        results.append(event)

                except BaseException as exc:
                    with result_lock:
                        failures.append(
                            (
                                index,
                                type(exc).__name__,
                                str(exc),
                            )
                        )

            threads = [
                threading.Thread(
                    target=worker,
                    args=(index,),
                    name=f"ac09-writer-{index}",
                )
                for index in range(writer_count)
            ]

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join(timeout=15)

            alive = [
                thread.name
                for thread in threads
                if thread.is_alive()
            ]

            self.assertEqual(
                alive,
                [],
                f"AC-09 concurrency fixture deadlocked: {alive}",
            )

            self.assertEqual(
                failures,
                [],
                f"concurrent writer failures: {failures}",
            )

            self.assertEqual(
                len(results),
                writer_count,
                "a concurrent append was lost",
            )

            files = sorted(
                ledger.glob("*.json")
            )

            self.assertEqual(
                len(files),
                writer_count,
                (
                    "ledger witness count differs from "
                    "successful append count"
                ),
            )

            events = [
                json.loads(
                    path.read_text(
                        encoding="utf-8"
                    )
                )
                for path in files
            ]

            sequences = [
                event["sequence"]
                for event in events
            ]

            self.assertEqual(
                sequences,
                list(
                    range(
                        1,
                        writer_count + 1,
                    )
                ),
                f"ledger sequence is not contiguous: {sequences}",
            )

            self.assertEqual(
                len(
                    {
                        event["sequence"]
                        for event in events
                    }
                ),
                writer_count,
                "duplicate sequence detected",
            )

            self.assertEqual(
                len(
                    {
                        event["event_id"]
                        for event in events
                    }
                ),
                writer_count,
                "duplicate event identifier detected",
            )

            expected_previous = None

            for sequence, (path, event) in enumerate(
                zip(files, events),
                start=1,
            ):
                self.assertTrue(
                    path.name.startswith(
                        f"{sequence:06d}_"
                    ),
                    (
                        "filename/sequence mismatch: "
                        f"{path.name}"
                    ),
                )

                self.assertEqual(
                    event[
                        "previous_event_sha512"
                    ],
                    expected_previous,
                    (
                        "broken predecessor linkage "
                        f"at sequence {sequence}"
                    ),
                )

                self.assertEqual(
                    event["event_sha512"],
                    event_digest(event),
                    (
                        "event digest mismatch "
                        f"at sequence {sequence}"
                    ),
                )

                expected_previous = (
                    event["event_sha512"]
                )

            leftovers = sorted(
                path.name
                for path in ledger.glob("*.tmp-*")
            )

            self.assertEqual(
                leftovers,
                [],
                (
                    "temporary witness files remain "
                    f"after publication: {leftovers}"
                ),
            )

            # Reconstruct from persisted state only.
            reconstructed = self.make_writer(
                ledger
            )

            self.assertEqual(
                reconstructed.sequence,
                writer_count,
            )

            self.assertEqual(
                reconstructed.head_sha512,
                events[-1]["event_sha512"],
            )

            self.assertEqual(
                reconstructed.event_ids,
                {
                    event["event_id"]
                    for event in events
                },
            )


if __name__ == "__main__":
    unittest.main()
