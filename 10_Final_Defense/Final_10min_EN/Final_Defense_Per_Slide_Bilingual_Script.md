# Final Defense Per-Slide Bilingual Script

This file is synchronized with the 18-slide PPT speaker notes. English speech is the main defense script; Chinese speech is for rehearsal reference.

## Slide 1. RISC-V Custom Instruction Based Lightweight CNN Accelerator FPGA Prototype Validation

Suggested time: 0:10-0:15

**English speech**

Good morning, everyone. My project is RISC-V Custom-Instruction CNN Accelerator on FPGA.

**Chinese speech**

闁告艾瀚紞鍛存嚀娴ｅ摜鐟庨柛姘嫰椤掔喖鏁嶇仦鑲╃憪闁告鐗嗛妶浠嬪Υ閸屾稑鐏夐柣銊ュ閵嗗秹鎯勯鑺バ﹂柍銉︾矊閻斺偓濞存粌鍐籌SC-V闁煎浜滈悾鐐▕婢跺鐦瑰ù鐘€楀▓鎱峃N闁告梻濞€閳ь剛鍠庡▍鎺楀灳濠靛嫧鍋?

## Slide 2. Presentation Outline

Suggested time: 0:30

**English speech**

I will present this project in three main parts. First, I will explain the motivation and project scope, so the target of the work is clear. Then I will introduce the system architecture and accelerator design. Finally, I will show the verification evidence and board results, including the CNN correctness test, the LeNet-5 sampled demo, the resource summary, and the limitations.

**Chinese speech**

闁哄牜鍓氶鐓幮ч崶銊バ撻柛鎺戞鐠愮喐绋夋径澶愬殝濞戞挻妲掗々锕傛焾閵娿儱鐎婚柕鍡楀€块々濠氬礂閸粎鐭欑紓浣哥Ф閻栬櫣绮氱捄鍝勑楅柡鍫濇惈閹风増銇勯崷顓熺獥闁肩厧鍟ú鍧楁晬鐏炵偓顫栫痪顓у枟濠€鐗堛亜閸︻厽绐楅悷鏇氱閻ｎ剟骞嬮幇顔界暠闁烩晩鍠楅悥锝夊Υ閸屾粌濮ч柛姘凹缁瑧绱掑鍥厙缂備胶鍠愰悘锕傚几閸曨偅瀚查柛鏃傚█閳ь剛鍠庡▍鎺旀媼閹规劦鍚€闁靛棗鍊瑰〒鍫曞触鎼达紕娼旂紒鈧ú顏嗗矗閻犲洣娴囬惁澶愬箲椤斿吋瀚查柡澶庢硶妤犲洨绱掗幘瀵镐函闁挎稑鑻€垫﹢骞忛悵绫扤婵繐绲块垾姗€骞€瑜庣粊瀵告嫚閺囨ǚ鍋撴稉銆哊et-5闂佹彃娲﹂悧鍗烆煶閺冨倶浠涢柕鍡曟祰缁侇偄鈹冮幇顓涘亾閼姐倗娉㈤柛婊冭嫰缂嶅宕滃澶嬵€欓柛鎺曠堪閳?

## Slide 3. Motivation and Objective

Suggested time: 0:08

**English speech**

I will first introduce the motivation of this project and define its scope.

**Chinese speech**

濡絾鐗曢崢娑欑鐎ｎ剛鐭濋柡鍫墴閵嗗秹鎯勯鐐暠闁活喗姊婚埞鎺楀礉閵婏附绨氶柨娑樿嫰閼荤喖寮版惔锝傗偓妯汇亜閸︻厽绐楅柤鐓庡暙濞插潡濡?

## Slide 4. Problem and Design Goal

Suggested time: 0:50

**English speech**

The problem I focus on is CNN convolution on a small embedded CPU. Convolution has many repeated multiply-accumulate operations, so running it only in software is not efficient, especially for edge devices with limited resources. RISC-V is useful here because it allows custom instructions. In this project, I use the NICE interface to connect a lightweight CNN accelerator to the E203 core. The goal is not to build a large ASIC-style accelerator, but to build a compact FPGA prototype and prove it step by step: first in RTL simulation, then in full SoC simulation, and finally on the FPGA board.

**Chinese speech**

闁哄牜鍓熼妴澶愬礂閾忣偅鏆堥柣銊ュ濡埖锛愬Ο缁樞﹂柛锔哄妼閻剟宕圭€ｎ亞銈甸柛蹇嬪劚缁鳖搲PU濞戞挸锕ユ晶鐣屾偘鐎涘┎N闁告顥撹ⅶ闁靛棗鍊稿畵搴ｇ矓椤栨艾鐦堕柛姘煎亜閵囧洭鏌岃箛娑樻濠㈣泛绉跺▓鎴炵▕濡偐鏌堥柛鏃傚Ь缁诲秶绮诲Δ瀣闁告瑯浜為弫銈嗘姜椤栨瑦顐介柟绗涘棭鏀介柡浣哥墢瀹稿吋绋夊澶屽蒋闁挎稑鑻幐銊╁礂閼稿灚笑闁革负鍔忕粊顐⑩攦閹邦厽绠掗梻鍕姉濞堟垶娼忛崷顓犲枠閻犱焦鍎抽ˇ顒佺▔婵炲簱鍋撴穱涓C-V闁汇劌瀚槐顓㈠礉閹稿孩笑闁衡偓椤栨稑鐦柤濂変簻閻ｇ偓绋婃径瀣樄濞寸姰鍊戦埀顒€鍊瑰﹢鐗堛亜閸︻厽绐楅梺顐ｄ亢缁诲儖ICE闁规亽鍎辫ぐ娑㈠箮婵犲懍姘﹂梺鎻掔箳妤犲構NN闁告梻濞€閳ь剛鍠庡▍鎺撴交閻愭潙澶嶉柛鎺旀203闁告劕鎳忛悧鎶藉Υ閸屾粍绐楅柡宥呮矗缁楀寮伴姘辨澖闁绘粍婢橀妵鍥垂婵狀枡IC缂佺嫏鍐潱闂侇偆鍠庡▍鎺楁晬瀹€鍐ｅ亾鐏炵偓笑闁哄瀚紓鎾舵瑜嶉崳楣冩儍閸戭敹GA闁告鍠庨悗鐑芥晬鐏炲€熷珯闂侇偅鍔栭鐐垫嫚娴ｈ顫栭悗鐟板暙瑜板弶绂掗妷銉ょ矗濞达絾绮ｇ槐浼村礂閸儮鍋撳宕囩畺RTL濞寸姾娉曞﹢锟犳晬鐏炶棄鏅欓梺顐ｄ亢缁诲啴宕楅埊绺狢濞寸姾娉曞﹢锟犳晬鐏炵偓浠橀柛姘濠€鐙GA鐎殿喒鍋撻柛娆愬灦濠㈡ɑ绋夋繝鍛閻炴稑琚埀?

## Slide 5. Project Scope and Deliverables

Suggested time: 0:50

**English speech**

This slide defines the scope I actually implemented. The project includes a 4 by 4 INT8 systolic PE array, six custom NICE instructions, integration with the Hummingbird E203 SoC, and validation on the Davinci Pro A7-100T FPGA board. The final deliverable is a repeatable FPGA prototype with evidence from RTL simulation, full-SoC simulation, and board testing. In the LeNet-5 demo, the convolution layers use NICE acceleration, while the rest of the program runs on E203 software.

**Chinese speech**

闁哄牜鍓熼妴澶愬及鎼达絺鈧ɑ銇勯崷顓熺獥闁肩厧鍟ú鍧楁晬鐏炶姤绀堝☉鎾跺劋閻︻垳鎷嬫ィ鍐╀粯閻熸洑鐒﹀﹢浣搞€掗崨顕呮閺夊牆婀遍弲顐﹀Υ閸屾氨鏉介梻鍕噹閻ゅ嫰鎮虫导鏉戝姤闁告帒妫楃€垫﹢骞?濞?闁汇劌鍤楴T8闁兼潙顦慨銖凟闂傚啴娼ч崹顏堝Υ?闁哄鎽侷CE闁煎浜滈悾鐐▕婢跺鐦瑰ù鐘€戦埀顑挎缁楀瓛ummingbird E203 SoC闁汇劌瀚板▔锕傚箣閹板墎绀夊ù鐘劚瀵兘宕烽垾鏄inci Pro A7-100T FPGA闁哄銇樼粭鍌炴儍閸曨垳宕ｉ悹鍥﹂檷閳ь剙鍊峰锔界濡吋绐楅柡宥呮处濡插憡绋夐埀顒佺▔椤忓嫬璁插璺虹Ф楠炲洭鎯冮崟顐㈡枾闁搞劌顑戠槐婵嬬嵁閼稿灚绠掑ù鐘烘硶濠€锟犲椽鐏炵偓绶茬紒鐙欏嫮銈撮悹鍥ㄦ礉閻﹀骞戦琛″亾閸屾瑧鐟濋柛鏍ф噺鐎氱懠SIC闁绘せ鏅濋幃濠勬媼閹规劦鍚€闁靛棔绀侀ˇ鍧楀冀閸涘﹤鈷栭悘鐐存磸閳ь兛绗㏄U缂佺嫏鍕ㄥ亾瑜戦崗妯盒掗弮鍥╃獩闁瑰瓨鐗滈弫鎾寸瑜忔鍥╃磽閺嶎剛妲柛锝冨妼娴兼劙宕楅悜鑺ユ嚑闁靛棗鍊稿﹢鐙秂Net-5婵犳洘姊婚妵姘▔椤撱劎绀夐柛娆樹簼濠€渚€宕℃骞繄浠﹂崒娆忊枏闁烩懇鍨稩CE闁告梻濞€閳ь剛鍣︾槐婵喰ч悩鎻掝嚙閻忕偛鍊搁幏浼村礂閵娿劎绠鹃柟鎭掑劚閻増绂掑鍥уЁ闁革腹鈧?03濞戞挸锕﹂弫杈ㄦ姜椤栨瑦顐介柟绗涘棭鏀介柕?

## Slide 6. System Architecture

Suggested time: 0:55

**English speech**

At the system level, the accelerator is connected to the E203 instruction path through NICE. This is different from a memory-mapped peripheral. The SoC includes the E203 RV32IMAC core, ITCM, DTCM, UART0, GPIO, and the CNN accelerator. Software sends operands through custom instructions, and the result returns through the processor register path. So from the software point of view, the accelerator is controlled like part of the instruction execution flow, not like a separate device with an address range. This keeps the control path simple and matches the custom-instruction goal of the project.

**Chinese speech**

濞寸姴娴烽柈瀵哥磼閻旈婀撮梻鍫涘灮濠€鍛存晬鐏炶棄顫ｉ梺顐ゅ枎濞呮帡鏌呭宕囩畺NICE閺夆晝鍋炵敮鎾礆閻?03闁汇劌瀚€垫碍绂掗妶澶嗗亾濮樺磭鐔呴柨娑樼焷閳ь剙濂旂粭澶愬及椤栨瑧绋婂☉鎾虫惈閸炲鈧稒蓱濡惭呬焊閸曨偒妯嗛悹浣峰嫎閳ь兛绺給C濞戞搩鍘肩€垫﹢骞忛悵?03 RV32IMAC闁告劕鎳忛悧鎶藉Υ娑擃摎CM闁靛棔绗峊CM闁靛棔绠扐RT0闁靛棔绗㏄IO闁告粌鐡擭N闁告梻濞€閳ь剛鍠庡▍鎺楀Υ閸屾繆鎷ù鐘茬埣閳ь剚淇虹换鍐嚊椤忓嫮鏆板☉鏂款槹鐎垫碍绂掗妶鍕倞闁稿繈鍎查幖閿嬫媴濠婂嫭娈堕柨娑樼灱缁劑寮稿鍫氬亾濮樺磭绠栧璺哄閹﹪宕抽妸銉ф閻庢稒锚濞呮帞鎹勯姘辩獮閺夆晜鏌ㄥú鏍Υ閸屾碍绀堟慨婵勫€撶划鐘虫姜椤栨瑦顐介悷娆愬笒鐎规娊鎯囩€ｅ墎绀夐柛鏃傚█閳ь剛鍠庡▍鎺楀磽韫囨梹笑闁圭娲ｉ幎銈夊箥瑜戦、鎴澝规担琛℃煠闁汇劌瀚粩鎾焾閵娿儱鐎婚柨娑樼焷閳ь剙濂旂粭澶愬及椤栨瑧顏卞☉鎿冧簼濠€渚€鎮鍌滃綄闁革附婢樺鍐嚑閸愩劍绾柣銊ュ椤﹁崵鎷嬫穱鎵佸亾閸屾繄绠归柡宥夋敱鐢爼宕氶幆鎵唴鐎垫澘瀚惁顔芥綇閸愵亝绾柟鎭掑劵缁辨繃绋婇悢渚剨闁告艾鐗婂﹢鐗堛亜閸︻厽绐楅柛鈺勬〃缁剟鎳涢鍕毎濞戞柨顦扮€垫碍绂掗妶鍥ㄧ暠閻犱焦宕橀鎼佹儎椤旂晫鍨奸柕?

## Slide 7. Accelerator Microarchitecture

Suggested time: 0:55

**English speech**

The accelerator core is a 4 by 4 PE array, so there are sixteen processing elements. Each PE performs signed INT8 multiplication and accumulates into an INT32 value. Weights are loaded by columns, and activation values are loaded by rows, which matches the packing of four INT8 values into one 32-bit operand. After the data is loaded, the computation produces partial sums, and a tree adder generates the final output. I chose this structure because it is small enough for the FPGA prototype, but it still demonstrates clear parallel acceleration compared with running the convolution completely on the CPU.

**Chinese speech**

闁告梻濞€閳ь剛鍠庡▍鎺楀冀缁嬭法濡囬柡?濞?闁汇劌鍤闂傚啴娼ч崹顏堟晬鐏炶偐顏遍柛蹇氶哺濠€?6濞戞搩浜滈ˇ鈺呮偠閸℃绀嬮柛蹇撳暔閳ь剙鍊归惁鈩冪▔閻欑竴闁圭瑳鍡╂斀闁哄牆顦遍渚€宕ｇ粙銕濼8濞戞梹蓱绾爼鏁嶇仦鍊熷珯缂侀硸鍨版慨鐐哄礆閻ф€32缂備焦鎸婚悘澶嬬▔椤撴壕鍋撻崒娑欑秬闂佹彃绉电€垫粓宕氬Δ鈧慨鐐存姜閺傘倗绀夐弶鍫熸尭閸欏棗鈹戦埀顒€煤鐠囨祴鍋撻崗鐓庣樆閻炴稑鑻慨鐐存姜閺傘倗绀夐弶鈺傜懁缁″啰鈧數鎳撶花鍙夌閸℃ê惟4濞戞挾瀚狽T8闁轰胶澧楁晶锕傚礌閸涙壆绠诲☉鎾亾濞?2濞达絽绉甸幖閿嬫媴濠婂嫭娈堕柣銊ュ閺岀喎顕ｈ箛瀣у亾閸屾稒娈堕柟璇″枛婵偞娼挊澶屾殮闁瑰瓨鍔曢幃妤呮晬瀹€鍕枅闁告帗銇炴鍥偨閻旂厧鍔ラ柛鎺戞閹蜂即鏁嶇仦钘夋櫃闁汇垼椴搁悥鑼躲亹閵忕姴顫ｆ繛澶嬫礀濞呮帒顕ュΔ鈧崺宀勫嫉閳ь剛绱掗崼锝囩炕闁告垶浜介埀顒€鍊块埀顒€顦扮€氥劍娼诲▎鎴綒缂備焦鎸婚悗顖炲及椤栨碍绀堝☉鎾虫惈閻ｇ姷鎼鹃崘宸閺夌偛顭烽崳娲晬瀹€鍕ㄥ亾閸屾碍鍊PGA闁告鍠庨悗鐑芥晬鐏炶姤鍊遍柡鍐╂构缁″啴鎳楅悾灞剧ゲ閻庣敻鈧稓鑹剧紒鍓ф瀸PU闁告顥撹ⅶ濞达絾鎸鹃獮鍥及鎼达絺鈧﹢鎯冮崟顐ュ珯閻炴稑鑻慨鐐烘焻閻斿憡娅忛柡瀣殠閳?

## Slide 8. Verification Evidence and Results

Suggested time: 0:08

**English speech**

Next, I will show the verification evidence and the measured board results.

**Chinese speech**

闁规亽鍎扮粭鍛村级閵夈儳娼旂紒鈧ú顏嗗矗閻犲洣娴囬惁澶愬箲椤斿吋瀚查悗鍦仱濡绢垶寮剁捄銊╃崜缂備焦鎸婚悘澶愬Υ?

## Slide 9. Why These Design Choices?

Suggested time: 0:55

**English speech**

These choices were made mainly for a lightweight FPGA prototype. A 4 by 4 PE array gives some parallelism but still fits easily on the A7-100T device, so it is suitable for a graduation project prototype. INT8 data is commonly used in small edge inference and also lets four 8-bit values fit into one 32-bit NICE operand, which reduces the number of load instructions. The output-stationary dataflow keeps partial sums local in the PEs and avoids unnecessary movement for this small convolution case. Using NICE avoids adding a memory-mapped bus interface and keeps the accelerator controlled directly by instructions.

**Chinese speech**

閺夆晜鐟ょ花铏规媼閹规劦鍚€闂侇偄顦扮€氥劍绋夐弰蹇ｆ矗闁哄牆绉存慨鐔哥鎼淬倓姘﹂梺鎻掔箳妤犲槕PGA闁告鍠庨悗鐑藉Υ?濞? PE闂傚啴娼ч崹顏堟嚄閼恒儱绲瑰〒姘◥缁斿鈧鑹鹃懟鐔烘偘鐏炶棄顔婇柨娑樿嫰閹捇寮張鐢电煗闁绘帟娉涜ぐ鍙夌閵夈劋姘﹂柡澶屽亾閺備線宕楅¨?-100T闁革絻鍔嬪▎銏ゆ晬瀹€鍕ㄥ亾閸屾碍鍊ゅù锝嗙矆鐠愮喖寮甸鍌ゆ綘婵絾娲濋鏇㈠储閻旈鈧兘濡存笟绋甌8閻㈩垰鎽滈弫銈嗙鎼达紕姣堥柛銊ヮ儓缁旂喓绱撳Ο璇茶吂闁荤偛妫寸槐婵囩▕閻旇鍘撮柟?濞?濞达絽绉甸弳鐔煎箥閹惧啿鐦堕弶鈺傜◥缁斿瓨绋?2濞达絽纭烮CE闁瑰灝绉崇紞鏃堝极鐢喚绀夊ù鐘叉唉閳ь剙鑻崳铏逛焊閹存繂顫ｉ弶鐐跺Г鐎垫碍绂掗妶鍡樻闂佹彃绻堥埀顒€鍊界欢顓㈠礄濞差亖鏁嗛柣锝嗙懄閺嗙喖骞戦鐣屻偊闁硅泛锕崕鎾礆閸℃瀚插ǎ鍥ㄧ箘閺嗏偓闁革腹澧闁告劕鎳橀崕鎾晬鐏炵瓔鍤犲ù婊冩唉缁绘牜绮斿鍛瘓闁告顥撹ⅶ闁革妇鍎ゅ▍娆撳矗椤栨瑤绨伴柛鎴濈箰閻垱绋夊鍛畱閻熸洑鑳跺▓鎴﹀极閻楀牆绁︾紒澶庮嚙婵晠濡撮崒娆忊枏闁烩懇鍨稩CE闁告瑯鍨禍鎺楁焼閸喖甯冲Λ鐗堢箓椤﹀鎯冮崟顐㈡暥閻庢稒蓱濡惭呬焊閸曨兘鍋撻懡銈呮疇闁规亽鍎辫ぐ娑㈡晬鐏炵厧鈻忛柛鏃傚█閳ь剛鍠庡▍鎺楁儎鐎涙ê澶嶉柣銏ｉ哺鐎垫碍绂掗妶鍡椾粯闁告帟缈伴埀?

## Slide 10. Implementation Flow

Suggested time: 0:45

**English speech**

The implementation was checked step by step instead of only testing the final board result. First, RTL tests were used to verify PE loading, COMP, and RSTAT behavior, because these are the basic operations of the accelerator. Then full-SoC simulation checked that the E203 core and the NICE accelerator worked together through the intended instruction path. After that, Vivado 2023.2 was used to build the FPGA prototype for the Davinci Pro A7-100T board. The final validation used UART output for software-visible results and ILA observation for signal-level context.

**Chinese speech**

閻庡湱鍋熼獮鍥ㄦ交閸モ斁鏌ら柡鍕靛灦閳ь剚鍔栭鐐搭殽瀹€鍐闁汇劌瀚哥槐婵嬫嚀鐏炶偐鐟濋柡鍕靛灠瑜把兠圭€ｎ厾妲搁柡鍫氬亾缂備礁鐗嗙槐鎴﹀矗閹寸偞绶茬紓浣规尰閻忓濡撮崒鐑嗘禃闁稿繐鐗忛弫顥窽L婵炴潙顑堥惁顖毼涢埀顒勫蓟椤ф湈闁告梻濮惧ù鍥Υ娑撳搵MP闁告粌顒⊿TAT閻炴稑濂旂拹鐔兼晬鐏炶姤绀堝☉鎾荤細缁绘牗绂嶅☉娆愋﹂柛鏃傚█閳ь剛鍠庡▍鎺楁儍閸曨偆鍞ㄩ柡鍫墯閹奸攱鎷呭┃搴撳亾閸屾粌濮ч柛姘叄閳ь剚淇虹换鍐礂閳釜C濞寸姾娉曞﹢锛勬兜椤旀鍚嘐203闁告劕鎳忛悧鎶藉椽鐎涒問CE闁告梻濞€閳ь剛鍠庡▍鎺楀矗椤栨瑤绨伴梺顐ｄ亢缁诲啯锛愰崟顒佸焸闁汇劌瀚€垫碍绂掗妶鍫㈢唴鐎垫澘瀚畷妤呭触鐏炴垝绱ｅù锝嗗殠閳ь剙鍊风粻锝夊触鎼存繂鈻忛柣鈶╂櫟ivado 2023.2濞戞挾鐦歛vinci Pro A7-100T鐎殿喒鍋撻柛娆愬灦濠㈡﹢鎮介悢绋跨亣FPGA闁告鍠庨悗鐑藉Υ閸屾稒浠樼紓浣哥墦閻涙瑧鎷犳担宄扮槣閻熸洑妞掔欢鐑芥閻曠枆RT閺夊牊鎸搁崵顓犳喆閸屾氨妾弶鐑嗗灟濞嗐垽宕ｉ婵愭綄缂備焦鎸婚悘澶愭晬鐏炲€熷珯闁烩懇鍟廘A闁圭粯鍔掔欢鍨┍閳ュ啿濞囩紒鐙欏倻鐟愬☉鎾愁儐閺嬪啴濡?

## Slide 11. FPGA Prototype Validation

Suggested time: 0:45

**English speech**

Before testing the accelerator result, I first confirmed that the FPGA prototype could boot and run firmware. The hello_e203 program printed boot, uart ok, and loop through UART. The ILA capture also showed that the CPU was executing in the ITCM code region. This result is basic, but it is important because if this part does not work, the accelerator result would not be meaningful. It proves that the CPU, memory initialization, clock, reset, and UART path were working together on the real FPGA board.

**Chinese speech**

闁革负鍔嶇粊瀵告嫚閺囩偛顫ｉ梺顐ゅ枎濞呮帞绱掗幘瀵镐函濞戞柨顑呮晶鐘绘晬鐏炴儳鐏夐柛蹇撶墢閳ユ鎷嬮ˉ鐞岹A闁告鍠庨悗鐑芥嚄閽樺妾柛姘煎灠婵晠鐛幆鎵閻炴稑鑻ù鎰闊祴鍋撴穱鐞玪lo_e203缂佸顑呯花顓㈡焻濮樺磭绠朥ART闁瑰灚鎸稿畵鍐╃閸濈ot闁靛棔鑿嘺rt ok闁告粌顔刼op闁靛棔鐥塋A闁规惌浜滃ù妯荤▕閻斿憡鈻旂紒鈧弧濂漊闁革腹鍟廡CM濞寸媴绲块悥婊堝礌閸濆嫮鍘甸柟绗涘棭鏀介柕鍡楀€界换鏍ㄧ▔椤忓棛娉㈤柡瀣矋閻︻喗娼忛崘銊у敤缁绢厸鍋撻柨娑樺缁叉儳顕ラ崼銉ユ閻熸洑绶ょ槐婵嬪炊閻樿精绀嬪┑鈥冲€归悘澶嬫交濞嗘挸鍔ラ柛鎺戞缁楀顔忛妷銈囩▕闁挎稑鑻幃妤呮閵忋垺鐣遍柛鏃傚█閳ь剛鍠庡▍鎺旂磼閹惧浜☉鏃傚枑閻ュ懘寮垫径瀣濞戞柨顦埀顒€鍊搁悾鐘垫嫚娴ｈ顫朇PU闁靛棔绀侀悺銊╁磼閵娿儲鐝ら柛鎺撶箓椤劙宕犻弽銉㈠亾娴ｈ顦ч梺鐣屽枂閳ь兛绀侀ˇ鍙夋媴瀹ュ懏瀚睻ART閻犱警鍨扮欢鐐哄捶閵娧勫焸閻庤妤稰GA鐎殿喒鍋撻柛娆愬灦濠㈡ɑ绋夋繝鍌氳濞寸姰鍎卞畷妤呭触鐏炴垝绱ｅù锝嗗殠閳?

## Slide 12. NICE Instruction Path Evidence

Suggested time: 0:45

**English speech**

This slide explains how firmware reaches the accelerator. The program issues CLEAR, WLOAD, DLOAD, COMP, and RSTAT as NICE custom instructions. These instructions cover clearing the accelerator state, loading weights and input data, starting computation, and reading back the result. So the accelerator is not only an isolated RTL module; it is called by software through the E203 instruction path, performs the computation, and returns a value that the CPU can read. This is the main connection between the hardware design and the board-level software result.

**Chinese speech**

闁哄牜鍓熼妴澶屾嫚鐎涙ɑ顫栭柛銉ㄦ〃濞嗐垺淇婇崒娆戠Э閻犱礁娼″Λ鍫曞礉閻樼儵鍋撻悢閿嬬彜闁靛棗鍊婚埢鍏兼償韫囨稈鍋撳宕囩畺NICE闁煎浜滈悾鐐▕婢跺鐦瑰ù鐘€曡ぐ鍌炲礄缁″EAR闁靛棔绠楲OAD闁靛棔绗峀OAD闁靛棔绔糘MP闁告粌顒⊿TAT闁靛棗鍊界换鏍ㄧ濞戞瑥鐦瑰ù鐘€曢崹搴ㄥ礆椤愩儺娲柣鈺傜墬缁旇崵绮氶崫鍕潱闂侇偆鍠庡▍鎺楁偐閼哥鍋撴担纰樺亾娴ｇ顫ｉ弶鐐跺Г濞煎牓鏌屽鍛閺夊牊鎸搁崣鍡涘极閻楀牆绁﹂柕鍡曠閹酣宕濋妸顭戝悁缂佺姵銇炴禍鎺楀矗婵犲拋鍤㈤柛銉у仧缁劑寮稿┃搴撳亾閸屾碍绀堟慨婵勫€曟慨鐐烘焻閻旈攱鐝ゅ☉鎾崇У濡插憡绋夐埀顒佺▔椤忓嫷鍔冪紒鏂款儑濞堟厾TL婵☆垪鈧櫕鍋ラ柨娑樼焷閳ь剙鏈Σ鎼佹偨鏉堫偉鎷ù鐘茬埣閳ь剚淇虹换鍍?03闁圭娲ｉ幎銈夋焻濮樺磭鐔呴悹瀣暟閺併倝鏁嶇仦鐣屾殮闁瑰瓨鍔橀鍝ョ不濡も偓閹娼婚弬鎸庣CPU闁告瑯鍨禍鎺旀嫚鐠囨彃绲块柣銊ュ缁劑寮稿┃搴撳亾閸屾繄绠归悘蹇氶哺濡插摜娑甸鎸庮偨閻犱焦宕橀鎼佸椽鐏炵偓绶茬紒鐙欏棜鎷ù鐘插缁劑寮稿鈧粻锝夋⒒鐎靛憡鐣卞☉鎾存椤╋附娼婚悙鏉戝闁?

## Slide 13. NICE Instruction Path Evidence: ILA Capture

Suggested time: 0:35

**English speech**

This page provides the ILA evidence for the same execution path. I do not need to explain every signal in the waveform, because the purpose here is not a waveform tutorial. The important point is that the board run was active and the processor was executing the expected firmware region. Together with the UART output, this supports that the result came from the actual FPGA execution flow, not only from a separate simulation or a software-only test.

**Chinese speech**

闁哄牜鍓熼妴澶愬箵閹邦亞杩旈柛姘缁旀挳骞嶈椤㈡垹鎹勯姘辩獮闁汇劌鍤楲A閻犲洣鐒﹀畵渚€濡撮崒婵堢闂佹彃濂旂粭澶愭閳ь剛鎲版笟鈧埀顒佸姃闁叉粎鎲撮敐澶婃珵婵炲鍨归懜鐗堢┍閳ュ啿濞囬柨娑樿嫰濞叉粍绋夐悜妯绘嫳濡炪倗鏁稿ú浼存儍閸曨亞鐟濋柡鍕靛灥椤斿鎲撮敐鍡楃毦鐟滈偊娼块埀顒€鍊块崳鎼佹倷鐟欏嫭笑鐎殿喒鍋撻柛娆愬灦濠㈡ɑ娼婚幇顖ｆ斀濠㈣泛瀚花顒勫嫉婢跺娅忛柣妯垮煐閳ь兛绶ょ槐婵囧緞閸曨厽鍊為柛锝冨妽椤掓粓宕烽妸锕€鈷旈悶娑樼焸椤ｂ晠寮甸悢鐑樼暠闁搞儴妗ㄥ▎銏ゅ礌閸濆嫮鍘甸柕鍡楀€荤划銊╁触閸︾潪RT閺夊牊鎸搁崵顓㈡晬鐏炶棄璁插ù鐘劜閺侇噣骞愭担鐣岀濞戞搩浜炵划銊╁几濠婂應鈧鈧湱鍋炲鐢告嚊椤忓棙鍩傞悗瑙勬シPGA闁圭瑳鍡╂斀婵炵繝鑳堕埢濂告晬瀹€鍐ｅ亾鐏炶偐鐟濋柛娆樹簼濡叉悂宕￠弴鐘差仾濞寸姾娉曞﹢锟犲箣閺嶎偄鍤遍弶鐑嗗灟濞嗐垹霉鐎ｎ厾妲搁柕?

## Slide 14. Board Result: CNN Correctness and Speedup

Suggested time: 0:55

**English speech**

This is the main reduced-CNN board result. The test is a 3 by 3 INT8 convolution over a 4 by 4 input. The software reference, the hardware accelerator output, and the expected output all match: 12, 23, 0, and 19. This confirms that the accelerator computes the same result as the reference for this test case. The cycle count also shows the performance difference. The CPU version takes 1,516 cycles, while the accelerator takes 287 cycles. So the measured convolution-only speedup is 5.282 times. I describe it as convolution-only because the measurement is for this kernel, not for the whole neural network.

**Chinese speech**

閺夆晜鐟﹀Σ鍛婄▔閺勫浚娲ｉ柣銊ュ閻ｆ繈宕犻張鍢歂闁哄娉曟鍥╃磼閹惧浜柕鍡楀€圭粊瀵告嫚閺囩偛鏁堕悗纭咁潐濡叉悂宕?濞?閺夊牊鎸搁崣鍡樼▔婵犲啫鈷旈悶?濞? INT8闁告顥撹ⅶ闁靛棗鍊介拏瀣鐠哄搫妫橀柤鏉垮暟缁劑寮稿┃搴撳亾娴ｈ　鈧牗绂掔捄鍝勵潱闂侇偆鍠庡▍鎺撴綇閹惧啿姣夐柛婊冩湰濠€锟犲嫉濞戞粎缈婚柛鎴炴そ閸忔ɑ绋夐埀顒勬嚊鏉堝墽绀夐柛鎺戞閸╁棝寮?2闁?3闁?闁?9闁靛棗鍊界换鏍嫚鐎涙ɑ顫栭柛锔哄姀椤曟艾霉鐎ｎ厾妲搁柣顫妺缁躲儲绋夐銊х闁告梻濞€閳ь剛鍠庡▍鎺旀媼閿涘嫮鏆紓浣规尰閻忓绋夋惔鈥虫闁兼澘鍟扮划銊╁几濠娾偓缁旀挳鎳涘ǎ顑藉亾閸屾碍鍣柡鍫㈠枑閺嗙喐绋婇悢椋庢綌缂佲偓鏉炴壆鍟婇柟顑棗鍘寸€瑰壊鍠栫槐鎾绘晬濞嗙爡U闁绘鐗婂﹢浼存閳ь剛鎲?516濞戞搩浜滈幊鍡涘嫉閻曞倻绀夐柛鏃傚█閳ь剛鍠庡▍鎺楁閳ь剛鎲?87濞戞搩浜滈幊鍡涘嫉閻旂补鍋撻崒姘婵縿鍊栫粊鏉戭嚗濡ゅ啯鐣卞ù鐘叉噹瀹撳海绮旈鐐插姤闁告帒妫楁慨鐐烘焻閻斿摜妲峰☉?.282闁稿﹤绉查埀顒€鍊界换鏍煂鐏炶棄绻侀悹瀣暕缁酣宕℃骞繈鏌堥妸銉ョ€婚柨娑樻湰濡叉悂宕堕悩杈閻犲洢鍎茬粊鎾煂韫囨稒瀚涢悗鐢殿攰缁绘牗绋夐鍕ス缂佸鍨遍悧鎶芥晬瀹€鍐ｅ亾鐏炶偐鐟濋柡鍕靛灡閺嗭絾绋夐鍡╂缂備礁绻掔紞澶岀磼濠у簱鍋?

## Slide 15. Board Result: LeNet-5 Inference

Suggested time: 0:45

**English speech**

To test a more complete workload, I also ran a LeNet-5 inference program on the FPGA. In this demo, NICE accelerates the convolution layers, while pooling and fully connected layers still run in software on E203. This means the demo checks system integration, not full hardware acceleration of every layer. The UART transcript records that all 10 sampled MNIST images were classified correctly. This should be understood as a sampled board demo, not as a full MNIST benchmark, but it still shows that the firmware, accelerator calls, and final classification flow can run together on the FPGA.

**Chinese speech**

濞戞捁妗ㄧ花鈥趁圭€ｎ厾妲搁柡鍥ㄦ綑閻ｎ剟寮€靛憡鐣辩€规悶鍎扮紞鏃傛嫻閻旂粯绁伴柨娑樻湰閸ㄦ粍绋婇悢閿嬭含FPGA濞戞挸锕ㄧ换宥囨偘鐏炶偐鍟奓eNet-5闁规亽鍔庨幃濠勭矙鐎ｎ亞纰嶉柕鍡楀€稿﹢顏呮交濞嗗酣鍤嬫繝鏇熸⒒閵囨碍绋夐銊хNICE闁告梻濞€閳ь剛鍠庡畵搴ｇ矓椤栨氨婀撮柨娑樻湰閻粓宕犻弽褏婀撮柛婊冭嫰閸欏繑娼婚悙鏉戝閻忕偛鍊风划娑㈡倿鐠虹儤韬珽203濞戞挸锕﹂弫杈ㄦ姜椤栨瑦顐介柟绗涘棭鏀介柕鍡楀€界换鏍箛韫囨挻鍤勯柣顐熷亾閻犲洢鍎茬槐銊х矆鏉炴澘鐦滈悷鏇氱窔閻涙瑧鎷犳担娲厙缂備胶鍠栧▔锕傚箣閹板墎绀夐柤鏉垮缁楀寮伴姘煎殸婵絽绻嬬粩瀵镐沪閸岀偛鍘撮弶鈺傜椤㈡垹娑甸鎸庮偨闁告梻濞€閳ь剛鍠嗛埀顑跨箖ART閻犱焦婢樼紞宥夊及閸撗佷粵10鐎殿喚濞€閸ｄ即寮界粙鐠慖ST闁搞儱澧芥晶鏍礂閵娾晛鍔ラ柛鎺戞鐞氼偄顫㈤敐鍥ｂ偓姗€濡撮崒婵堢闂佹彃鐭傚〒鍓佹啺娴ｈ顫栫痪顓у櫙缁辨繃娼诲▎蹇撴锭闁哄嫷鍨堕崳浼村冀闁垮绶茬紒鐙欏嫮宸濈紒鈧悮瀵哥濞戞挸绉靛Σ鍝モ偓鐟版湰閺嗩枔NIST闁糕晛鎼崳顖毭圭€ｎ厾妲搁柨娑樺缁插墽鈧懓鍟╃划娑㈡倿閹偊鍤涢柡鍕濞存劖绂掗煬娴嬪亾娴ｇ顫ｉ梺顐ゅ枎濞呮帞鎷崘顏呮殢闁告粌鏈〒鍓佺磼閸繂鐎荤紒顐ょ帛缁侊妇绮欑€ｎ亜璁插ù鐘劚濠€鐙GA濞戞挸锕ｇ粩瀵告導閻ゎ垳绠ラ悶娑樿閳?

## Slide 16. Performance and Resource Summary

Suggested time: 0:45

**English speech**

This slide summarizes performance, resource usage, and timing evidence. The measured convolution-only speedup is 5.282 times, meeting the target of at least 5 times. The resource usage also fits comfortably on the A7-100T FPGA: LUT is 20.8 percent, FF is 10.1 percent, BRAM is 26.3 percent, and DSP is 0 percent. On the right, I added the routed Vivado timing evidence: the cnn_sysclk_ila build reports WNS of 12.472 ns, WHS of 0.057 ns, and zero failing endpoints. So this implementation is not only functionally correct, but also timing-clean in the tested FPGA configuration.

**Chinese speech**

闁哄牜鍓熼妴澶愬箑閼姐倗娉㈠☉鎾存椤╋箓寮悧鍫濈ウ闁靛棗鍊圭粊鏉戭嚗濡ゅ啯鐣卞ù鐘叉噹瀹撳海绮旈鐐插姤闁告帒妫楁慨鐐烘焻閻斿摜妲峰☉?.282闁稿﹤绋勭槐婵囨綇閹冪厒闁告顥撹ⅶ闁哄秵鐡曢崵锔句焊?闁稿﹤绉存慨鐐烘焻閻旂儤鐣遍柣鈺婂枟閻栵綁濡存笟鐮匞A闁哄瀚紓鎾诲籍鐠鸿櫣纰嶉柡鈧懜鍨異闁挎稑鐣眓n_sysclk_ila闁哄瀚紓鎾绘儍閸掑S濞?2.472缂佹儳纾～妤呮晬瀹€鍐惧殯闁哄嫬娴峰ú浼村冀閸ャ劍顦ч梺鐣屽枍缁楀懏绂掑鍡樼畳闁哄啳娉涚花顓熸媴濞嗘挸娅ら柕鍡楀€界粊顐⑩攦閹邦亜鈻忛柣顫妺缁″啫袙閺冨洨绐涢梺顐㈠€烽懙鎴︽晬濮濃偓UT濞?0.8%闁挎稑鐡桭濞?0.1%闁挎稑鐡揜AM濞?6.3%闁挎稑鐡昐P濞?%闁挎稑鑻ú婊勭▔閻戞ɑ鎷遍悹浣瑰礃椤撶鈻介埄鍐╃畳濞达綀娉曢弫顥猄P闁秆勵殙缁绘鎮扮仦鑲╊啋婵炲娲忛埀顒€鍊界换鏍ㄧ濞戞瑦娈堕柟璇″枦椤曗晠寮版惔銈庡殙FPGA濞戞挸锕ｇ划娑㈠嫉婢跺顏遍悗瑙勬皑閳规牠姊荤€靛憡鏆忓ù婊冮閹绱掗鐔封挅閻忕偞娲忛埀?

## Slide 17. Limitations and Future Work

Suggested time: 0:45

**English speech**

There are still several limitations. The SoC currently runs at 16 MHz, so a higher frequency would require timing re-validation. The 10 out of 10 MNIST result is only a sampled demo, so broader testing is still needed before making a stronger accuracy claim. Also, only Conv1 and Conv2 use NICE; pooling and fully connected layers remain on the software side, which limits the end-to-end speed. Future work can include a larger MNIST subset, FC acceleration, RSTAT optimization to reduce readback overhead, and more formal checks for the NICE interface.

**Chinese speech**

鐟滅増鎸告晶鐘垫媼閹规劦鍚€濞寸姴绉靛﹢渚€宕欓悩閬嶅殝闂傚嫭鍔曢崺妤呭Υ娣囦抗C闁烩晩鍠栨晶鐘虫交閹邦垼鏀介柛?6 MHz闁挎稑鑻々褔寮稿鍡╂矗闁圭粯鍔欓悵顔斤紣閹寸姴鑺抽柨娑樼焸濞撳墎鎲版笟鈧崳鎼佸棘閹峰瞼绠婚悶娑樻湰濡炲倹鎯旇箛娑氬矗閻犲洣闄嶉埀?0鐎殿喚鍤朜IST闁稿繈鍔戦崕鏉戭潰閿濆洠鈧﹢宕ｉ鍛﹂梺鎻掓处閻楀崬顭抽弮鍌樹粵闁挎稑鑻﹢顏堝箵閹邦剙姣夐柡鍥ㄦ綑瀹搁亶鎯冮崟顐㈡珯缁绢収鍠氬鑲╃磼閹捐鍟堥柛鎾崇С缁盯鎮為崼鏇熶粯閻熸洑鐒﹀ú鎸庡緞瑜戦～澶娢熼埄鍐偞閻犲洦娲忛埀顒€鍊歌ぐ鐔稿緞閺嶇數绀夐柛娆樹簼濠€涓唎nv1闁告粌鐡攐nv2濞达綀娉曢弫顥碔CE闁挎稑鏈惈婊堝礌閺嵮呮勾闁告粌鑻崣蹇旀交閻愭潙澶嶉悘鐐插€风划娑㈡倿鐠虹儤韬弶鐑嗗灟濞嗐垺绗熻缁诲秶鎮板畝瀣閺夆晜鐟╁娲礆閺堢數鍟婄紒鏃戝灠閸╁瞼绮╅鐐╁亾閻斿嘲顔婇柕鍡楀€瑰﹢顓㈠级閵夈儰绱ｅù锝嗙矊瑜板弶绂掗妷銉ョ樁闁瑰鍓氬ú鎸庡緞瑜忓▓鎱歂IST閻庢稒鍔欏▔锕€霉鐎ｎ厾妲搁柕鍡曠閸欏繑娼婚悙鏉戝閻忕偛鍊告慨鐐烘焻閻旂补鍋撴笟鈧埀顒佷亢缁诲儛STAT濞村吋锚鐎垫煡宕欒箛鎾舵瘜閻犲洩顕уú鏍ь嚕閳ь剟鏌ㄩ埀顒勬晬鐏為棿绨伴柛娆忥工椤曠攩ICE闁规亽鍎辫ぐ娑欐交濞戞粠鏀介柡鍥ㄦ綑閼告澘顕ｈ箛鎾愁嚙闁汇劌瀚ˉ鍛村蓟閵夛絺鍋?

## Slide 18. Brief Summary

Suggested time: 0:35-0:45

**English speech**

To summarize, this project integrates a lightweight INT8 CNN accelerator with the E203 RISC-V core through NICE custom instructions. The prototype was validated from RTL simulation to FPGA board execution, using UART output and ILA captures as evidence. The board results show correct reduced-CNN output, 5.282 times convolution-only speedup, and a 10 out of 10 sampled LeNet-5 demo. The main value of the project is that it connects the accelerator design with a working RISC-V SoC and real FPGA evidence. Thank you for listening. I am happy to take questions.

**Chinese speech**

闁哄牃鍋撻柛姘閳ь剝宕电划銊︾▔閳ь剚绋夌€ｅ墎绀夐柡鍫墴閵嗗秹鎯勯鈧埀顒佷亢缁诲儖ICE闁煎浜滈悾鐐▕婢跺鐦瑰ù鐘€х槐婵堜焊閸℃矮姘﹂梺鎻掔箳妤犲様NT8 CNN闁告梻濞€閳ь剛鍠庡▍鎺楁⒖閸℃ê鐏囬柛鎺旀203 RISC-V闁告劕鎳忛悧铏▔椤撴壕鍋撻崒姘枾闁搞劌顑勭划鐕玊L濞寸姾娉曞﹢鈩冾殽瀹€鍐闁告帞妾礟GA闁哄娉曟鍥箥瑜戦、鎴︽晬鐏炲€熷珯濞达綀娉曢弫顥籄RT閺夊牊鎸搁崵顓㈠椽鐎涙湙A闁规惌浜滃ù妯绘媴濠娾偓鐠愮喓鎷犳担鐟扮ウ闁靛棗鍊瑰妯肩棯瑜忕划銊╁几濠婂嫭鈻旂紒鈧悮瀵哥缂佺姭鍋撻柛鏍ㄦ缚NN閺夊牊鎸搁崵顓烆潰閿濆洠鈧﹢鏁嶇仦钘夌ス缂佸鍨堕崕鎾礆閸℃顫ｉ梺顐ゅ枑閻︻喗绋?.282闁稿﹤绋勭槐婵嬬嵁鐠鸿櫣鏆氶柟瀛樺姃缁?0鐎殿喚濞€閸ｄ即寮界粙鐞玁et-5闁搞儱澧芥晶鏍儍閸曨剦鍔€缁绢収鍠栭崹搴ｇ尵缂佹宸濈紒鈧幁鎺嗗亾閸屾稒鎷卞銈呮贡濞蹭即鎯冮崟顏勭槣閻熸洑妞掗悳顖炲磹閻撳孩韬ù婊冨婵℃悂宕濋悩鐑╁亾閻旈攱鐝ら悹浣瑰礃椤撴悂濡存担绋胯鐎规悶鍎扮紞鏃堟儍閸戠SC-V SoC闁告粌鐬煎﹢锛勨偓瑙勬シPGA閻犲洣鐒﹀畵浣规交閻愭潙澶嶉悹褔鏀卞鐢稿Υ閸屾繈妯嬮悹瀣ㄥ灩閹洦鎷呭鍫氬亾娴ｅ摜鐟庨柛姘嫰椤掔喖鏁嶇仦鎯х亯闁汇劌瀚惇褰掑箮閵壯呮尝闁哄鍣︾槐婵嗏枎閵忥絿绠ｉ柟缁樺姍濡爼濡?
