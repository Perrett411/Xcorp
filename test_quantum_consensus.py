import asyncio
import numpy as np
import pytest
from quantum_consensus import QuantumConsensusFunction


@pytest.fixture
def qcf():
    return QuantumConsensusFunction(min_nodes=2, max_nodes=8, max_load=100)


def test_init_defaults():
    qcf = QuantumConsensusFunction()
    assert qcf.node_range == (8, 64)
    assert qcf.active_nodes == 8
    assert qcf.max_load == 100
    assert np.isclose(qcf.coherence_time, 1e-9)
    assert np.isclose(qcf.superposition_angle, np.pi / 2)


def test_init_custom():
    qcf = QuantumConsensusFunction(min_nodes=4, max_nodes=16, max_load=200)
    assert qcf.node_range == (4, 16)
    assert qcf.active_nodes == 4
    assert qcf.max_load == 200


def test_adjust_nodes_high_load(qcf):
    result = asyncio.run(qcf.adjust_nodes(80))
    # 2 + (8-2)*0.80 = 6.8 → int = 6
    assert result == 6
    assert qcf.active_nodes == 6


def test_adjust_nodes_low_load(qcf):
    result = asyncio.run(qcf.adjust_nodes(10))
    # 2 + (8-2)*0.10 = 2.6 → int = 2, equals min_nodes
    assert result == qcf.node_range[0]
    assert qcf.active_nodes == qcf.node_range[0]


def test_adjust_nodes_full_load(qcf):
    result = asyncio.run(qcf.adjust_nodes(100))
    # 100/100 * 8 = 8, clamped to max 8
    assert result == qcf.node_range[1]


def test_adjust_nodes_clamp_to_max(qcf):
    result = asyncio.run(qcf.adjust_nodes(200))
    assert result == qcf.node_range[1]


def test_entangle_nodes_circuit_structure(qcf):
    qcf.active_nodes = 3
    circuit = asyncio.run(qcf.entangle_nodes(None))
    assert circuit.num_qubits == 3
    # Circuit should have H + 2*CX + 2*RZ = 5 gates
    op_names = [instr.operation.name for instr in circuit.data]
    assert op_names.count('h') == 1
    assert op_names.count('cx') == 2
    assert op_names.count('rz') == 2


def test_validate_consensus_returns_bool(qcf):
    qcf.active_nodes = 2
    circuit = asyncio.run(qcf.entangle_nodes(None))
    result = asyncio.run(qcf.validate_consensus(circuit))
    assert isinstance(result, bool)


def test_validate_consensus_bell_state(qcf):
    """Bell state should achieve consensus (two dominant states)."""
    qcf.active_nodes = 2
    circuit = asyncio.run(qcf.entangle_nodes(None))
    result = asyncio.run(qcf.validate_consensus(circuit))
    assert result is True


def test_validate_consensus_ghz_state(qcf):
    """GHZ state across 4 qubits should achieve consensus."""
    qcf.active_nodes = 4
    circuit = asyncio.run(qcf.entangle_nodes(None))
    result = asyncio.run(qcf.validate_consensus(circuit))
    assert result is True


def test_full_async_workflow():
    """Test the full async workflow: adjust nodes → entangle → validate."""
    async def run():
        qcf = QuantumConsensusFunction(min_nodes=2, max_nodes=4, max_load=100)
        await qcf.adjust_nodes(50)
        circuit = await qcf.entangle_nodes(None)
        return await qcf.validate_consensus(circuit)

    result = asyncio.run(run())
    assert isinstance(result, bool)
