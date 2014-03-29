OpenERP-Stock-QC
======================

OpenERP 质量控制 / 质量管理模块


　　每次给客户演示完 OpenERP 系统，都会被问到：质量控制模块是什么样子的？ OpenERP 官方给出的解决方案有两个：一是链式库位（凡到达此库位的产品均可自动生成质检移库操作），另一个是拉式流（建立了拉式流的产品，自动根据规则生成质检移库操作）。官方这个质检其实只是增加一个内部移库操作，记录的信息很少，也不直观，更不便于授权给质量控制部门单独操作。当演示完这两个质量控制方案，客户的眼神总会流露出神秘的信息：你这是在忽悠我吧？

　　好在增加一个直观的质量控制模块也并非什么难事：修改工作流，在入仓前加插一个状态，再记录一些必要的质检信息即可满足一般的使用要求。对要求高的客户，可以在此基础上进一步扩充，做成质量管理子系统。

　　这样做的结果虽然强制了所有入仓的产品均需要检验，但也简化了使用流程，无论是否使用多仓库和多库位，都能正常进行质量控制（官方的方案必须使用多仓库和多库位），这对于小公司尤其有用，他们不必开启多仓库和多库位的选项就能进行质量控制。

	详情请看：http://zhsunlight.cn/openerp-stock-qc.html