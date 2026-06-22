# Mathlib 4.30 Trace-Corpus Preflight

- Verdict: `needs_attention`
- Input: `/workspace/thymic_project/paper/iclr_2/outputs/phase3_second_stage_eval_goals_500.jsonl`
- Mathlib root: `/workspace/thymic_project/paper/iclr_2/repos/mathlib4_lean430`
- Goals checked: 500
- Unique declaration names checked: 2538
- Missing declaration names: 9

## Goal-Level Audit

| Item | Count | Rate |
|---|---:|---:|
| `file_exists` | 497 | 99.4% |
| `module_inferred` | 500 | 100.0% |
| `theorem_name_present` | 500 | 100.0% |
| `theorem_exists_in_mathlib430` | 494 | 98.8% |
| `all_proof_core_exists_in_mathlib430` | 498 | 99.6% |
| `target_name_in_proof_core` | 0 | 0.0% |
| `target_name_in_candidates` | 500 | 100.0% |

## Missing Names

- `AffineSpace.StarConvex.smul_vadd_mem_of_isClosed_of_mem_asymptoticCone`
- `CategoryTheory.Presheaf.Sheaf.Presieve.FamilyOfElements.Presheaf.GrothendieckTopology.ofArrows_mem_iff_isLocallySurjective_cofanIsColimitDesc_uliftYoneda_map`
- `FermatLastTheoremForThreeGen.Solution.associated_of_dvd_a_add_b_of_dvd_a_add_eta_sq_mul_b`
- `MeasureTheory.ProbabilityTheory.Kernel.isProjectiveLimit_trajFun`
- `Tactic.ComputeAsymptotics.MultiseriesExpansion`
- `Tactic.ComputeAsymptotics.MultiseriesExpansion.Multiseries`
- `Tactic.ComputeAsymptotics.MultiseriesExpansion.Multiseries.Multiseries.Multiseries.Sorted.Sorted.Approximates.elim_cons`
- `compl_riemannZetaZeros_mem_codiscrete`
- `self_sdiff_frontier`

## Readout

- Name-level migration has issues or circular-leakage risks. Inspect the samples before building a full replay grid.

## Risk Samples

### missing_file

- `mathlib4::lp.Memℓp.holder_gen_bound` theorem=`lp.Memℓp.holder_gen_bound` file=`Mathlib/Analysis/Normed/Lp/lpHolder.lean`
- `mathlib4::Right.div_le_div_iff₀` theorem=`Right.div_le_div_iff₀` file=`Mathlib/Algebra/Order/GroupWithZero/Basic.lean`
- `mathlib4::Real.exists_nat_pos_inv_lt` theorem=`Real.exists_nat_pos_inv_lt` file=`Mathlib/Algebra/Order/Archimedean/Real/Basic.lean`

### missing_theorem_name

- `mathlib4::CategoryTheory.Presheaf.Sheaf.Presieve.FamilyOfElements.Presheaf.GrothendieckTopology.ofArrows_mem_iff_isLocallySurjective_cofanIsColimitDesc_uliftYoneda_map` theorem=`CategoryTheory.Presheaf.Sheaf.Presieve.FamilyOfElements.Presheaf.GrothendieckTopology.ofArrows_mem_iff_isLocallySurjective_cofanIsColimitDesc_uliftYoneda_map` file=`Mathlib/CategoryTheory/Sites/LocallySurjective.lean`
- `mathlib4::Tactic.ComputeAsymptotics.MultiseriesExpansion.Multiseries.Multiseries.Multiseries.Sorted.Sorted.Approximates.elim_cons` theorem=`Tactic.ComputeAsymptotics.MultiseriesExpansion.Multiseries.Multiseries.Multiseries.Sorted.Sorted.Approximates.elim_cons` file=`Mathlib/Tactic/ComputeAsymptotics/Multiseries/Defs.lean`
- `mathlib4::MeasureTheory.ProbabilityTheory.Kernel.isProjectiveLimit_trajFun` theorem=`MeasureTheory.ProbabilityTheory.Kernel.isProjectiveLimit_trajFun` file=`Mathlib/Probability/Kernel/IonescuTulcea/Traj.lean`
- `mathlib4::compl_riemannZetaZeros_mem_codiscrete` theorem=`compl_riemannZetaZeros_mem_codiscrete` file=`Mathlib/NumberTheory/LSeries/ZetaZeros.lean`
- `mathlib4::AffineSpace.StarConvex.smul_vadd_mem_of_isClosed_of_mem_asymptoticCone` theorem=`AffineSpace.StarConvex.smul_vadd_mem_of_isClosed_of_mem_asymptoticCone` file=`Mathlib/Topology/Algebra/AsymptoticCone.lean`
- `mathlib4::FermatLastTheoremForThreeGen.Solution.associated_of_dvd_a_add_b_of_dvd_a_add_eta_sq_mul_b` theorem=`FermatLastTheoremForThreeGen.Solution.associated_of_dvd_a_add_b_of_dvd_a_add_eta_sq_mul_b` file=`Mathlib/NumberTheory/FLT/Three.lean`

### missing_proof_core

- `mathlib4::Tactic.ComputeAsymptotics.MultiseriesExpansion.Multiseries.Multiseries.Multiseries.Sorted.Sorted.Approximates.elim_cons` theorem=`Tactic.ComputeAsymptotics.MultiseriesExpansion.Multiseries.Multiseries.Multiseries.Sorted.Sorted.Approximates.elim_cons` file=`Mathlib/Tactic/ComputeAsymptotics/Multiseries/Defs.lean`
- `mathlib4::mem_interior_iff_notMem_frontier` theorem=`mem_interior_iff_notMem_frontier` file=`Mathlib/Topology/Closure.lean`

### target_in_proof_core

- None.

### target_in_candidates

- `mathlib4::Submodule.Module.Finite.of_equiv_equiv` theorem=`Submodule.Module.Finite.of_equiv_equiv` file=`Mathlib/RingTheory/Finiteness/Basic.lean`
- `mathlib4::finsum_mem_mul` theorem=`finsum_mem_mul` file=`Mathlib/Algebra/BigOperators/Finprod.lean`
- `mathlib4::AlgebraicGeometry.HasAffineProperty.affineAnd_le_affineAnd` theorem=`AlgebraicGeometry.HasAffineProperty.affineAnd_le_affineAnd` file=`Mathlib/AlgebraicGeometry/Morphisms/AffineAnd.lean`
- `mathlib4::Ideal.IsDedekindDomain.ramificationIdx_ne_zero` theorem=`Ideal.IsDedekindDomain.ramificationIdx_ne_zero` file=`Mathlib/NumberTheory/RamificationInertia/Ramification.lean`
- `mathlib4::Module.rank_tensorProduct'` theorem=`Module.rank_tensorProduct'` file=`Mathlib/LinearAlgebra/Dimension/Constructions.lean`
- `mathlib4::FirstOrder.Language.definableFun_const` theorem=`FirstOrder.Language.definableFun_const` file=`Mathlib/ModelTheory/Definability.lean`
- `mathlib4::MeasureTheory.Measure.compProd_apply_univ` theorem=`MeasureTheory.Measure.compProd_apply_univ` file=`Mathlib/Probability/Kernel/Composition/MeasureCompProd.lean`
- `mathlib4::Ideal.IsNoetherianRing.of_prime` theorem=`Ideal.IsNoetherianRing.of_prime` file=`Mathlib/RingTheory/Noetherian/OfPrime.lean`
- `mathlib4::Polynomial.splits_X_sub_C_mul_iff` theorem=`Polynomial.splits_X_sub_C_mul_iff` file=`Mathlib/Algebra/Polynomial/Splits.lean`
- `mathlib4::LocalizedModule.LocalizedModule.IsLocalizedModule.lift_comp` theorem=`LocalizedModule.LocalizedModule.IsLocalizedModule.lift_comp` file=`Mathlib/Algebra/Module/LocalizedModule/Basic.lean`
