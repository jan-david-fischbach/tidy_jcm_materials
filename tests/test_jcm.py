from pathlib import Path

import jcmwave
import numpy as np
from tidy3d import material_library

from tidy_jcm_materials.generate import gen_material

folder = Path(__file__).parent


def test_generate_jcm_materials():
    tidy_mat = material_library["Ag"]["JohnsonChristy1972"]
    mat = gen_material(tidy_mat, domain_id=2)

    omegas = np.linspace(2e15, 6e15, 50)
    jcmwave.daemon.shutdown()
    jcmwave.daemon.add_workstation("localhost", Multiplicity=5, NThreads=1)

    jobs = []
    for omega in omegas:
        keys = {"Omega": omega, "material": mat}
        job = jcmwave.solve(
            str(folder / "test_jcm/get_material.jcmp"),
            keys,
            working_dir=f"{folder}/test_jcm/mat/omega_{omega}",
        )
        jobs.append(job)

    res, log = jcmwave.daemon.wait(jobs)

    errors = [msg["Log"]["Error"] for msg in log]
    for err in errors:
        if err != "":
            raise RuntimeError(err)

    eps = []
    for r in res:
        eps.append(r[1]["field"][0][0])
    eps_jcm = np.array(eps)

    eps_tidy = tidy_mat.eps_model(omegas / (2 * np.pi))

    assert np.allclose(eps_jcm, eps_tidy)
