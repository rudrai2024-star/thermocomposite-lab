# 05 — Scientific Methodology and Equations

Let `Vf` be fibre fraction and `Vm=1−Vf`. The core uses mixture estimates:

`E1=Vf Ef+Vm Em` (Voigt); `E2=(Vf/Ef+Vm/Em)^−1`; `G12=(Vf/Gf+Vm/Gm)^−1`.

`α1=Vf αf+Vm αm`; `α2=(Vf αf/Ef+Vm αm/Em)/(Vf/Ef+Vm/Em)`.

Thermal free strain is `εth=αΔT`; fully restrained uniaxial stress is `σrest=−E1α1ΔT`. The implemented curve samples constant-property estimates over a temperature interval; model temperatures are kelvin, while UI display may convert. These equations do not establish calibrated performance across materials or temperatures.

Built-in values are reference estimates, not sourced certified allowables. The implementation validates material/fraction/temperature/boundary conditions and can invoke CLT. There is no statistical uncertainty propagation, experimental fitting, or transient heat-transfer model. Test formulas are in [07](07_Composite_Testing_Laboratory.md); laminate formulation is in [06](06_Classical_Laminate_Theory.md).
