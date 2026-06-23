# Mathlib 4.30 Trace-Corpus Preflight

- Verdict: `needs_attention`
- Input: `/workspace/thymic_project/paper/iclr_2/outputs/phase3_second_stage_eval_fold0_goals_500.jsonl`
- Mathlib root: `/workspace/thymic_project/paper/iclr_2/repos/mathlib4_lean430`
- Goals checked: 500
- Unique declaration names checked: 2600
- Missing declaration names: 14

## Goal-Level Audit

| Item | Count | Rate |
|---|---:|---:|
| `file_exists` | 497 | 99.4% |
| `module_inferred` | 500 | 100.0% |
| `theorem_name_present` | 500 | 100.0% |
| `theorem_exists_in_mathlib430` | 487 | 97.4% |
| `all_proof_core_exists_in_mathlib430` | 499 | 99.8% |
| `target_name_in_proof_core` | 0 | 0.0% |
| `target_name_in_candidates` | 500 | 100.0% |

## Missing Names

- `AffineSpace.asymptoticCone_sUnion`
- `AlgebraicGeometry.ProjectiveSpectrum.StructureSheaf.SectionSubring.ProjectiveSpectrum.homogeneousLocalizationToStalk_stalkToFiberRingHom`
- `Bundle.Bundle.Trivialization.contMDiffWithinAt_section`
- `CategoryTheory.Yoneda.ULiftYoneda.Coyoneda.ULiftCoyoneda.Functor.uliftCoyonedaEquiv_symm_map`
- `ChevalleyThm.PolynomialC.InductionObj.MvPolynomialC.chevalley_mvPolynomial_mvPolynomial`
- `Mathlib.Tactic.Simp.Nat.Ico_zero`
- `MeasureTheory.measure_sdiff_lt_of_lt_add`
- `Metric.EMetric.Metric.le_infDist`
- `Pi.Function.Pi.mulSingle_le_mulSingle`
- `Pi.MulHom.Pi.mulSingle_commute`
- `PiNat.exists_nat_nat_continuous_surjective_of_completeSpace`
- `ProbabilityTheory.MeasureTheory.Measure.eq_of_cdf`
- `QuotientGroup.AddSubgroup.norm_trivial_quotient_mk`
- `conj_commutatorElement_right_commutatorElement_mul`

## Readout

- Name-level migration has issues or circular-leakage risks. Inspect the samples before building a full replay grid.

## Risk Samples

### missing_file

- `mathlib4::Bound.one_lt_mul` theorem=`Bound.one_lt_mul` file=`Mathlib/Algebra/Order/GroupWithZero/Basic.lean`
- `mathlib4::SimpleGraph.chromaticNumber_le_card` theorem=`SimpleGraph.chromaticNumber_le_card` file=`Mathlib/Combinatorics/SimpleGraph/Coloring/Vertex.lean`
- `mathlib4::ProbabilityTheory.bernoulliMeasure_real_apply` theorem=`ProbabilityTheory.bernoulliMeasure_real_apply` file=`Mathlib/Probability/Distributions/Bernoulli.lean`

### missing_theorem_name

- `mathlib4::Pi.Function.Pi.mulSingle_le_mulSingle` theorem=`Pi.Function.Pi.mulSingle_le_mulSingle` file=`Mathlib/Algebra/Order/Pi.lean`
- `mathlib4::Mathlib.Tactic.Simp.Nat.Ico_zero` theorem=`Mathlib.Tactic.Simp.Nat.Ico_zero` file=`Mathlib/Tactic/Simproc/FinsetInterval.lean`
- `mathlib4::ProbabilityTheory.MeasureTheory.Measure.eq_of_cdf` theorem=`ProbabilityTheory.MeasureTheory.Measure.eq_of_cdf` file=`Mathlib/Probability/CDF.lean`
- `mathlib4::QuotientGroup.AddSubgroup.norm_trivial_quotient_mk` theorem=`QuotientGroup.AddSubgroup.norm_trivial_quotient_mk` file=`Mathlib/Analysis/Normed/Group/Quotient.lean`
- `mathlib4::PiNat.exists_nat_nat_continuous_surjective_of_completeSpace` theorem=`PiNat.exists_nat_nat_continuous_surjective_of_completeSpace` file=`Mathlib/Topology/MetricSpace/PiNat.lean`
- `mathlib4::Metric.EMetric.Metric.le_infDist` theorem=`Metric.EMetric.Metric.le_infDist` file=`Mathlib/Topology/MetricSpace/HausdorffDistance.lean`
- `mathlib4::AlgebraicGeometry.ProjectiveSpectrum.StructureSheaf.SectionSubring.ProjectiveSpectrum.homogeneousLocalizationToStalk_stalkToFiberRingHom` theorem=`AlgebraicGeometry.ProjectiveSpectrum.StructureSheaf.SectionSubring.ProjectiveSpectrum.homogeneousLocalizationToStalk_stalkToFiberRingHom` file=`Mathlib/AlgebraicGeometry/ProjectiveSpectrum/StructureSheaf.lean`
- `mathlib4::Bundle.Bundle.Trivialization.contMDiffWithinAt_section` theorem=`Bundle.Bundle.Trivialization.contMDiffWithinAt_section` file=`Mathlib/Geometry/Manifold/VectorBundle/Basic.lean`
- `mathlib4::Pi.MulHom.Pi.mulSingle_commute` theorem=`Pi.MulHom.Pi.mulSingle_commute` file=`Mathlib/Algebra/Group/Pi/Lemmas.lean`
- `mathlib4::CategoryTheory.Yoneda.ULiftYoneda.Coyoneda.ULiftCoyoneda.Functor.uliftCoyonedaEquiv_symm_map` theorem=`CategoryTheory.Yoneda.ULiftYoneda.Coyoneda.ULiftCoyoneda.Functor.uliftCoyonedaEquiv_symm_map` file=`Mathlib/CategoryTheory/Yoneda.lean`

### missing_proof_core

- `mathlib4::MeasurableSet.exists_isCompact_sdiff_lt` theorem=`MeasurableSet.exists_isCompact_sdiff_lt` file=`Mathlib/MeasureTheory/Measure/Regular.lean`

### target_in_proof_core

- None.

### target_in_candidates

- `mathlib4::Nat.multinomial_congr_of_eq_on_inter` theorem=`Nat.multinomial_congr_of_eq_on_inter` file=`Mathlib/Data/Nat/Choose/Multinomial.lean`
- `mathlib4::Quaternion.continuous_im` theorem=`Quaternion.continuous_im` file=`Mathlib/Analysis/Quaternion.lean`
- `mathlib4::Orientation.tan_oangle_sub_right_of_oangle_eq_pi_div_two` theorem=`Orientation.tan_oangle_sub_right_of_oangle_eq_pi_div_two` file=`Mathlib/Geometry/Euclidean/Angle/Oriented/RightAngle.lean`
- `mathlib4::ContDiffOn.union_of_isOpen` theorem=`ContDiffOn.union_of_isOpen` file=`Mathlib/Analysis/Calculus/ContDiff/Basic.lean`
- `mathlib4::Pi.Function.Pi.mulSingle_le_mulSingle` theorem=`Pi.Function.Pi.mulSingle_le_mulSingle` file=`Mathlib/Algebra/Order/Pi.lean`
- `mathlib4::Mathlib.Tactic.Simp.Nat.Ico_zero` theorem=`Mathlib.Tactic.Simp.Nat.Ico_zero` file=`Mathlib/Tactic/Simproc/FinsetInterval.lean`
- `mathlib4::Algebra.Presentation.relation_comp_localizationAway_inl` theorem=`Algebra.Presentation.relation_comp_localizationAway_inl` file=`Mathlib/RingTheory/Extension/Presentation/Basic.lean`
- `mathlib4::Matrix.sum_sum_single` theorem=`Matrix.sum_sum_single` file=`Mathlib/Data/Matrix/Basis.lean`
- `mathlib4::Filter.tendsto_comp_val_Ioi_atTop` theorem=`Filter.tendsto_comp_val_Ioi_atTop` file=`Mathlib/Order/Filter/AtTopBot/Basic.lean`
- `mathlib4::Filter.map_const_principal_coprod_map_id_principal` theorem=`Filter.map_const_principal_coprod_map_id_principal` file=`Mathlib/Order/Filter/Prod.lean`
