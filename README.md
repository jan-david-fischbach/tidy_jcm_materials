# tidy_jcm_materials 0.1.1

Converts materials from tidy3d database to JCMwave compatible pole residue format

## Usage

``` python
from tidy3d import material_library
from tidy_jcm_materials.generate import gen_material

tidy_mat = material_library["Ag"]["JohnsonChristy1972"]
mat = gen_material(tidy_mat, domain_id=2, name="gold")
```
