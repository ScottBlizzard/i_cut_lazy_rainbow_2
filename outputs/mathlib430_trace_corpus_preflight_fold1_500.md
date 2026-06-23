# Mathlib 4.30 Trace-Corpus Preflight

- Verdict: `needs_attention`
- Input: `/workspace/thymic_project/paper/iclr_2/outputs/phase3_second_stage_eval_fold1_goals_500.jsonl`
- Mathlib root: `/workspace/thymic_project/paper/iclr_2/repos/mathlib4_lean430`
- Goals checked: 500
- Unique declaration names checked: 2360
- Missing declaration names: 15

## Goal-Level Audit

| Item | Count | Rate |
|---|---:|---:|
| `file_exists` | 493 | 98.6% |
| `module_inferred` | 500 | 100.0% |
| `theorem_name_present` | 500 | 100.0% |
| `theorem_exists_in_mathlib430` | 489 | 97.8% |
| `all_proof_core_exists_in_mathlib430` | 498 | 99.6% |
| `target_name_in_proof_core` | 0 | 0.0% |
| `target_name_in_candidates` | 500 | 100.0% |

## Missing Names

- `Bundle.Bundle.Trivialization.mdifferentiableWithinAt_totalSpace_iff`
- `CategoryTheory.Limits.BinaryBicones.BinaryBicone.Bicone.biprod.opIso_inv_inr_op`
- `CharTwo.neg_one_eq_one_iff`
- `Mathlib.Meta.Positivity.Int.preimage_Ioc`
- `Mathlib.Meta.Positivity.LucasLehmer.X.closed_form`
- `Mathlib.Tactic.Simp.Nat.Iio_succ_eq_of_Icc_zero_eq`
- `Order.Concept.extent_iInf`
- `Order.strictMono_of_lt_add_one`
- `Pi.MulHom.Function.Pi.Sigma.uncurry_mulSingle_mulSingle`
- `ProbabilityTheory.IsPreBrownianReal`
- `ProbabilityTheory.IsPreBrownianReal.neg`
- `closure_subset_mul_left_of_mem_nhds_one_of_inv`
- `sdiv_eq_one_iff_eq`
- `sdiv_smul_eq_sdiv_div`
- `smul_sdiv_assoc`

## Readout

- Name-level migration has issues or circular-leakage risks. Inspect the samples before building a full replay grid.

## Risk Samples

### missing_file

- `mathlib4::ProbabilityTheory.IsPreBrownianReal.neg` theorem=`ProbabilityTheory.IsPreBrownianReal.neg` file=`Mathlib/Probability/BrownianMotion/Basic.lean`
- `mathlib4::Module.Dual.exists_extension_of_le_seminorm` theorem=`Module.Dual.exists_extension_of_le_seminorm` file=`Mathlib/Analysis/LocallyConvex/HahnBanach.lean`
- `mathlib4::LinearMap.index_of_surjective` theorem=`LinearMap.index_of_surjective` file=`Mathlib/Algebra/Module/LinearMap/Index.lean`
- `mathlib4::Set.sdiv_smul_comm` theorem=`Set.sdiv_smul_comm` file=`Mathlib/Algebra/Torsor/Basic.lean`
- `mathlib4::Submodule.ClosedComplemented.of_finiteDimensional` theorem=`Submodule.ClosedComplemented.of_finiteDimensional` file=`Mathlib/Analysis/LocallyConvex/HahnBanach.lean`
- `mathlib4::Left.mul_pos` theorem=`Left.mul_pos` file=`Mathlib/Algebra/Order/GroupWithZero/Basic.lean`
- `mathlib4::NNReal.Real.one_le_sqrt` theorem=`NNReal.Real.one_le_sqrt` file=`Mathlib/Analysis/Real/Sqrt.lean`

### missing_theorem_name

- `mathlib4::Pi.MulHom.Function.Pi.Sigma.uncurry_mulSingle_mulSingle` theorem=`Pi.MulHom.Function.Pi.Sigma.uncurry_mulSingle_mulSingle` file=`Mathlib/Algebra/Group/Pi/Lemmas.lean`
- `mathlib4::ProbabilityTheory.IsPreBrownianReal.neg` theorem=`ProbabilityTheory.IsPreBrownianReal.neg` file=`Mathlib/Probability/BrownianMotion/Basic.lean`
- `mathlib4::closure_subset_mul_left_of_mem_nhds_one_of_inv` theorem=`closure_subset_mul_left_of_mem_nhds_one_of_inv` file=`Mathlib/Topology/Algebra/Group/Pointwise.lean`
- `mathlib4::Mathlib.Meta.Positivity.Int.preimage_Ioc` theorem=`Mathlib.Meta.Positivity.Int.preimage_Ioc` file=`Mathlib/Algebra/Order/Floor/Ring.lean`
- `mathlib4::Mathlib.Tactic.Simp.Nat.Iio_succ_eq_of_Icc_zero_eq` theorem=`Mathlib.Tactic.Simp.Nat.Iio_succ_eq_of_Icc_zero_eq` file=`Mathlib/Tactic/Simproc/FinsetInterval.lean`
- `mathlib4::Mathlib.Meta.Positivity.LucasLehmer.X.closed_form` theorem=`Mathlib.Meta.Positivity.LucasLehmer.X.closed_form` file=`Mathlib/NumberTheory/LucasLehmer.lean`
- `mathlib4::Order.strictMono_of_lt_add_one` theorem=`Order.strictMono_of_lt_add_one` file=`Mathlib/Algebra/Order/SuccPred.lean`
- `mathlib4::Bundle.Bundle.Trivialization.mdifferentiableWithinAt_totalSpace_iff` theorem=`Bundle.Bundle.Trivialization.mdifferentiableWithinAt_totalSpace_iff` file=`Mathlib/Geometry/Manifold/VectorBundle/MDifferentiable.lean`
- `mathlib4::Order.Concept.extent_iInf` theorem=`Order.Concept.extent_iInf` file=`Mathlib/Order/Concept.lean`
- `mathlib4::CategoryTheory.Limits.BinaryBicones.BinaryBicone.Bicone.biprod.opIso_inv_inr_op` theorem=`CategoryTheory.Limits.BinaryBicones.BinaryBicone.Bicone.biprod.opIso_inv_inr_op` file=`Mathlib/CategoryTheory/Limits/Shapes/BinaryBiproducts.lean`

### missing_proof_core

- `mathlib4::ProbabilityTheory.IsPreBrownianReal.neg` theorem=`ProbabilityTheory.IsPreBrownianReal.neg` file=`Mathlib/Probability/BrownianMotion/Basic.lean`
- `mathlib4::Set.sdiv_smul_comm` theorem=`Set.sdiv_smul_comm` file=`Mathlib/Algebra/Torsor/Basic.lean`

### target_in_proof_core

- None.

### target_in_candidates

- `mathlib4::FirstOrder.Language.presburger.isSemilinearSet_formula_realize_semilinear` theorem=`FirstOrder.Language.presburger.isSemilinearSet_formula_realize_semilinear` file=`Mathlib/ModelTheory/Arithmetic/Presburger/Definability.lean`
- `mathlib4::Computation.destruct_eq_think` theorem=`Computation.destruct_eq_think` file=`Mathlib/Data/Seq/Computation.lean`
- `mathlib4::ArithmeticFunction.IsMultiplicative.Nat.Coprime.sum_divisors_mul` theorem=`ArithmeticFunction.IsMultiplicative.Nat.Coprime.sum_divisors_mul` file=`Mathlib/NumberTheory/ArithmeticFunction/Misc.lean`
- `mathlib4::StandardBorelSpace.MeasureTheory.Measurable.MeasurableSet.image_of_monotoneOn` theorem=`StandardBorelSpace.MeasureTheory.Measurable.MeasurableSet.image_of_monotoneOn` file=`Mathlib/MeasureTheory/Constructions/Polish/Basic.lean`
- `mathlib4::CharP.natCast_eq_natCast` theorem=`CharP.natCast_eq_natCast` file=`Mathlib/Algebra/CharP/Basic.lean`
- `mathlib4::Polynomial.bernoulli_comp_one_sub_X` theorem=`Polynomial.bernoulli_comp_one_sub_X` file=`Mathlib/NumberTheory/BernoulliPolynomials.lean`
- `mathlib4::PiNat.disjoint_cylinder_of_longestPrefix_lt` theorem=`PiNat.disjoint_cylinder_of_longestPrefix_lt` file=`Mathlib/Topology/MetricSpace/PiNat.lean`
- `mathlib4::IsLocallyClosed.image` theorem=`IsLocallyClosed.image` file=`Mathlib/Topology/LocallyClosed.lean`
- `mathlib4::Polynomial.roots_def` theorem=`Polynomial.roots_def` file=`Mathlib/Algebra/Polynomial/Roots.lean`
- `mathlib4::Module.Basis.addHaar_reindex` theorem=`Module.Basis.addHaar_reindex` file=`Mathlib/MeasureTheory/Measure/Haar/OfBasis.lean`
