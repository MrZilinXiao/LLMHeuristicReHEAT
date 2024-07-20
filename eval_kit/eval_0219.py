# Evaluation toolkit for 0219 version dataset evaluation.
import os
import re
import json
from typing import List, Dict, Tuple

def route_to_eval_func(problem_id: int):
    return globals()[f'eval_problem_{problem_id}']

def presence_eval(response: str, gold: str, ignore_case=True):
    if ignore_case:
        response = response.lower()
        gold = gold.lower()
    return gold in response

def ranking_eval(response: str, gold_ranking: List[str]):
    """
    gold_ranking is a list of strings whose order is the correct ranking for gt
    """
    id_to_spans = {}
    for it in re.finditer(r'\[(\d+)\]', response):
        id_to_spans[it.group(1)] = it.span()
    try:
        for rank_idx in gold_ranking:
            assert rank_idx in id_to_spans.keys()
        # make sure gold ranking appears in the same order as in the response
        return all(
            id_to_spans[prev_rank_idx][0] < id_to_spans[rank_idx][0]
            for prev_rank_idx, rank_idx in zip(gold_ranking, gold_ranking[1:])
        )
    except (KeyError, AssertionError):
        return False


def choice_eval(response: str, positives: List, negatives: List[str]):
    return any(presence_eval(response, positive) for positive in positives) and not any(
        presence_eval(response, negative) for negative in negatives
    )

def dependancy_eval(response: str, gold: str):
    # leave for pairs like problem 0 & 1
    raise NotImplementedError


def eval_problem_0(response):
    return ranking_eval(response, ["2", "4"])

def eval_problem_1(response: str):
    # repeat the option number & the option itself is acceptable
    return choice_eval(response, 
                       positives=["[2]", "less than 50 percent"], 
                       negatives=["[1]", "greater than 50 percent"]
                       )

def eval_problem_2(response: str):
    return choice_eval(response, ["[1]", "greater than 50 percent"], ["[2]", "less than 50 percent"])

def eval_problem_3(response: str):
    return choice_eval(response, ["[2]", "less than 50 percent"], ["[1]", "greater than 50 percent"])

def eval_problem_4(response: str):
    return choice_eval(response, ["[1]", "greater than 50 percent"], ["[2]", "less than 50 percent"])

def eval_problem_5(response: str):
    return choice_eval(response, ["[2]", "less than 50 percent"], ["[1]", "greater than 50 percent"])

def eval_problem_6(response: str):
    return choice_eval(response, ["[1]", "greater than 50 percent"], ["[2]", "less than 50 percent"])

def eval_problem_7(response: str):
    return choice_eval(response, ["[2]", "less than 50 percent"], ["[1]", "greater than 50 percent"])

def eval_problem_8(response: str):
    return choice_eval(response, ["[1]", "greater than 50 percent"], ["[2]", "less than 50 percent"])

def eval_problem_9(response: str):
    return choice_eval(response, ["[1]", "science major"], ["[2]", "humanities major"])

# ----------------- label 12- -----------------

def eval_problem_10(response: str):
    return choice_eval(response, ["[2]", "humanities major"], ["[1]", "science major"])

def eval_problem_11(response: str):
    return choice_eval(response, ["[1]", "technician"], ["[2]", "manager"])

def eval_problem_12(response: str):
    return choice_eval(response, ["[2]", "manager"], ["[1]", "technician"])

def eval_problem_13(response: str):
    return choice_eval(response, ["[2]", "financial sector workers"], ["[1]", "creative sector workers"])

def eval_problem_14(response: str):
    return choice_eval(response, ["[1]", "creative sector workers"], ["[2]", "financial sector workers"])

def eval_problem_15(response: str):
    return choice_eval(response, ["[1]", "automobile user"], ["[2]", "bicycle user"])

def eval_problem_16(response: str):
    return choice_eval(response, ["[2]", "bicycle user"], ["[1]", "automobile user"])

def eval_problem_17(response: str):
    return choice_eval(response, ["[1]", "apartment"], ["[2]", "detached house"])

def eval_problem_18(response: str):
    return choice_eval(response, ["[2]", "detached house"], ["[1]", "apartment"])

def eval_problem_19(response: str):
    return choice_eval(response, ["[1]", "doctor/nurse"], ["[2]", "administrator/manager"])

def eval_problem_20(response: str):
    return choice_eval(response, ["[2]", "administrator/manager"], ["[1]", "doctor/nurse"])

def eval_problem_21(response: str):
    return choice_eval(response, ["[1]", "crew/ground service member"], ["[2]", "corporate executive"])

def eval_problem_22(response: str):
    return choice_eval(response, ["[2]", "corporate executive"], ["[1]", "crew/ground service member"])

def eval_problem_23(response: str):
    return choice_eval(response, ["[2]", "local resident"], ["[1]", "out-of-town visitor"])

def eval_problem_24(response: str):
    return choice_eval(response, ["[1]", "out-of-town visitor"], ["[2]", "local resident"])

def eval_problem_25(response: str):
    return choice_eval(response, ["[1]", "sales/cashier"], ["[2]", "safety/maintenance person"])

def eval_problem_26(response: str):
    return choice_eval(response, ["[2]", "safety/maintenance person"], ["[1]", "sales/cashier"])

def eval_problem_27(response: str):
    return choice_eval(response, ["[2]", "general outpatient clinic"], ["[1]", "emergency clinic"])

def eval_problem_28(response: str):
    return choice_eval(response, ["[1]", "emergency clinic"], ["[2]", "general outpatient clinic"])

def eval_problem_29(response: str):
    return choice_eval(response, ["[2]", "traditional extracurricular activity"], ["[1]", "robotics club"])

def eval_problem_30(response: str):
    return choice_eval(response, ["[1]", "robotics club"], ["[2]", "traditional extracurricular activity"])

def eval_problem_31(response: str):
    return choice_eval(response, ["[1]", "local resident"], ["[2]", "immigrant from another city"])

def eval_problem_32(response: str):
    return choice_eval(response, ["[2]", "immigrant from another city"], ["[1]", "local resident"])

def eval_problem_33(response: str):
    return choice_eval(response, ["[1]", "undergraduate student"], ["[2]", "graduate student"])

def eval_problem_34(response: str):
    return choice_eval(response, ["[2]", "graduate student"], ["[1]", "undergraduate student"])

def eval_problem_35(response: str):
    return choice_eval(response, ["[1]", "technology development/engineering"], ["[2]", "marketing/human resources"])

def eval_problem_36(response: str):
    return choice_eval(response, ["[2]", "marketing/human resources"], ["[1]", "technology development/engineering"])

def eval_problem_37(response: str):
    return choice_eval(response, ["[1]", "technology development/engineering"], ["[2]", "marketing/human resources"])

def eval_problem_38(response: str):
    return choice_eval(response, ["[2]", "marketing/human resources"], ["[1]", "technology development/engineering"])

def eval_problem_39(response: str):
    return choice_eval(response, ["[2]", "marketing/human resources"], ["[1]", "technology development/engineering"])

def eval_problem_40(response: str):
    return choice_eval(response, ["[1]", "sports program"], ["[2]", "arts and drama club"])

def eval_problem_41(response: str):
    return choice_eval(response, ["[2]", "arts and drama club"], ["[1]", "sports program"])

def eval_problem_42(response: str):
    return choice_eval(response, ["[1]", "sports program"], ["[2]", "arts and drama club"])

def eval_problem_43(response: str):
    return choice_eval(response, ["[2]", "arts and drama club"], ["[1]", "sports program"])

def eval_problem_44(response: str):
    return choice_eval(response, ["[2]", "arts and drama club"], ["[1]", "sports program"])

def eval_problem_45(response: str):
    return ranking_eval(response, ["7", "8"])

def eval_problem_46(response: str):
    return ranking_eval(response, ["2", "1"])

def eval_problem_47(response: str):
    return ranking_eval(response, ["3", "4", "7"])

def eval_problem_48(response: str):
    return ranking_eval(response, ["3", "6"])

def eval_problem_49(response: str):
    return ranking_eval(response, ["3", "6"])

def eval_problem_50(response: str):
    return ranking_eval(response, ["3", "6", "8"])

def eval_problem_51(response: str):
    return ranking_eval(response, ["5", "7"])

def eval_problem_52(response: str):
    return ranking_eval(response, ["3", "7"])

def eval_problem_53(response: str):
    return ranking_eval(response, ["3", "1"])

def eval_problem_54(response: str):
    return ranking_eval(response, ["1", "2"]) & ranking_eval(response, ["3", "2"]) & ranking_eval(response, ["4", "2"])

def eval_problem_55(response: str):
    return ranking_eval(response, ["1", "2"]) & ranking_eval(response, ["3", "2"]) & ranking_eval(response, ["1", "4"]) & ranking_eval(response, ["3", "4"])

def eval_problem_56(response: str):
    return presence_eval(response, "[1]")

def eval_problem_57(response: str):
    return presence_eval(response, "[1]")

def eval_problem_58(response: str):
    return choice_eval(response, ["[1]", "Mr. F. has had one or more heart attacks"], ["[2]", "55 years old Mr. F. has had one or more heart attacks"])

def eval_problem_59(response: str):
    return choice_eval(response, ["[1]", "Mr. F. has had one or more heart attacks"], ["[2]", "Mr. F has had one or more heart attacks and Mr. G. is over 55 years old"])

def eval_problem_60(response: str):
    return presence_eval(response, "[1]")

def eval_problem_61(response: str):
    return ranking_eval(response, ["3", "4"]) & ranking_eval(response, ["2", "4"])

def eval_problem_62(response: str):
    return ranking_eval(response, ["3", "7"]) & ranking_eval(response, ["4", "7"])

def eval_problem_63(response: str):
    return ranking_eval(response, ["3", "6"])

def eval_problem_64(response: str):
    return ranking_eval(response, ["3", "6"])

def eval_problem_65(response: str):
    return ranking_eval(response, ["3", "4", "7"])

def eval_problem_66(response: str):
    return ranking_eval(response, ["3", "6"])

def eval_problem_67(response: str):
    return ranking_eval(response, ["3", "6"])

def eval_problem_68(response: str):
    return ranking_eval(response, ["4", "7"]) & ranking_eval(response, ["3", "7"])

def eval_problem_69(response: str):
    return ranking_eval(response, ["3", "6"])

def eval_problem_70(response: str):
    return ranking_eval(response, ["3", "6"])

def eval_problem_71(response: str):
    return ranking_eval(response, ["3", "7"]) & ranking_eval(response, ["4", "7"])

def eval_problem_72(response: str):
    return ranking_eval(response, ["3", "6"])

def eval_problem_73(response: str):
    return ranking_eval(response, ["2", "6"])

def eval_problem_74(response: str):
    return ranking_eval(response, ["1", "4", "7"])

def eval_problem_75(response: str):
    return ranking_eval(response, ["3", "6"])

def eval_problem_76(response: str):
    return ranking_eval(response, ["1", "4", "6"])

def eval_problem_77(response: str):
    return ranking_eval(response, ["1", "8"]) & ranking_eval(response, ["2", "8"]) & ranking_eval(response, ["1", "7"]) & ranking_eval(response, ["5", "7"])

def eval_problem_78(response: str):
    return ranking_eval(response, ["3", "5"])

def eval_problem_79(response: str):
    return ranking_eval(response, ["1", "5"]) & ranking_eval(response, ["7", "5"]) & ranking_eval(response, ["9", "2"])

def eval_problem_80(response: str):
    return ranking_eval(response, ["6", "4"])

def eval_problem_81(response: str):
    return ranking_eval(response, ["1", "4"]) & ranking_eval(response, ["1", "7"]) & ranking_eval(response, ["6", "4"]) & ranking_eval(response, ["9", "7"])

def eval_problem_82(response: str):
    return ranking_eval(response, ["5", "3"]) & ranking_eval(response, ["8", "6"])

def eval_problem_83(response: str):
    return ranking_eval(response, ["1", "6"]) & ranking_eval(response, ["1", "8"]) & ranking_eval(response, ["4", "8"])

def eval_problem_84(response: str):
    return ranking_eval(response, ["1", "6"]) & ranking_eval(response, ["4", "8"])

def eval_problem_85(response: str):
    return ranking_eval(response, ["1", "6"]) & ranking_eval(response, ["1", "8"]) & ranking_eval(response, ["5", "6"]) & ranking_eval(response, ["2", "8"])

def eval_problem_86(response: str):
    return ranking_eval(response, ["1", "2"]) & ranking_eval(response, ["1", "7"]) & ranking_eval(response, ["5", "2"]) & ranking_eval(response, ["10", "7"])

def eval_problem_87(response: str):
    return ranking_eval(response, ["4", "1"])

def eval_problem_88(response: str):
    return ranking_eval(response, ["1", "2"]) & ranking_eval(response, ["4", "2"]) & ranking_eval(response, ["1", "6"]) & ranking_eval(response, ["8", "6"])

def eval_problem_89(response: str):
    return ranking_eval(response, ["2", "6"]) & ranking_eval(response, ["8", "7"])

def eval_problem_90(response: str):
    return ranking_eval(response, ["1", "5"]) & ranking_eval(response, ["2", "5"]) & ranking_eval(response, ["1", "7"]) & ranking_eval(response, ["10", "7"])

def eval_problem_91(response: str):
    return ranking_eval(response, ["1", "6"]) & ranking_eval(response, ["7", "6"])

def eval_problem_92(response: str):
    return presence_eval(response, "[2]")

def eval_problem_93(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_94(response: str):
    return presence_eval(response, "[2]")

def eval_problem_95(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_96(response: str):
    return presence_eval(response, "[2]")

def eval_problem_97(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_98(response: str):
    return presence_eval(response, "[2]")

def eval_problem_99(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_100(response: str):
    return presence_eval(response, "[2]")

def eval_problem_101(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_102(response: str):
    return presence_eval(response, "[2]")

def eval_problem_103(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_104(response: str):
    return presence_eval(response, "[2]")

def eval_problem_105(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_106(response: str):
    return presence_eval(response, "[2]")

def eval_problem_107(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_108(response: str):
    return presence_eval(response, "[2]")

def eval_problem_109(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_110(response: str):
    return presence_eval(response, "[2]")

def eval_problem_111(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_112(response: str):
    return presence_eval(response, "[2]")

def eval_problem_113(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_114(response: str):
    return presence_eval(response, "[2]")

def eval_problem_115(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_116(response: str):
    return presence_eval(response, "[2]")

def eval_problem_117(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_118(response: str):
    return presence_eval(response, "[2]")

def eval_problem_119(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_120(response: str):
    return presence_eval(response, "[2]") or presence_eval(response, "[4]")

def eval_problem_121(response: str):
    return ranking_eval(response, ["2", "1"]) or ranking_eval(response, ["4", "3"])

def eval_problem_122(response: str):
    return presence_eval(response, "[2]") 

def eval_problem_123(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_124(response: str):
    return presence_eval(response, "[4]") or presence_eval(response, "[2]")

def eval_problem_125(response: str):
    return ranking_eval(response, ["2", "1"]) or ranking_eval(response, ["4", "3"])

def eval_problem_126(response: str):
    return presence_eval(response, "[4]")

def eval_problem_127(response: str):
    return ranking_eval(response, ["4", "3", "2", "1"])

def eval_problem_128(response: str):
    return presence_eval(response, "[2]")

def eval_problem_129(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_130(response: str):
    return presence_eval(response, "[2]")

def eval_problem_131(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_132(response: str):
    return presence_eval(response, "[2]")

def eval_problem_133(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_134(response: str):
    return presence_eval(response, "[2]")

def eval_problem_135(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_136(response: str):
    return presence_eval(response, "[2]")

def eval_problem_137(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_138(response: str):
    return presence_eval(response, "[2]")

def eval_problem_139(response: str):
    return ranking_eval(response, ["2", "1", "4", "3"])

def eval_problem_140(response: str):
    return presence_eval(response, "[2]")

def eval_problem_141(response: str):    
    return presence_eval(response, "[2]")

def eval_problem_142(response: str):
    return presence_eval(response, "[2]")

def eval_problem_143(response: str):
    return presence_eval(response, "[2]")

def eval_problem_144(response: str):
    return presence_eval(response, "[4]")

def eval_problem_145(response: str):
    return presence_eval(response, "[2]")

def eval_problem_146(response: str):
    return presence_eval(response, "[2]")

def eval_problem_147(response: str):
    return presence_eval(response, "[2]")

def eval_problem_148(response: str):
    return presence_eval(response, "[2]")

def eval_problem_149(response: str):
    return presence_eval(response, "[2]")

def eval_problem_150(response: str):
    return presence_eval(response, "[1]")

def eval_problem_151(response: str):
    return presence_eval(response, "[2]")

def eval_problem_152(response: str):
    return presence_eval(response, "[1]")

def eval_problem_153(response: str):
    return presence_eval(response, "[2]")

def eval_problem_154(response: str):
    return presence_eval(response, "[2]")

def eval_problem_155(response: str):
    return presence_eval(response, "[1]")

def eval_problem_156(response: str):
    return presence_eval(response, "[1]")

def eval_problem_157(response: str):
    return presence_eval(response, "[1]")

def eval_problem_158(response: str):
    return presence_eval(response, "[2]")

def eval_problem_159(response: str):
    return presence_eval(response, "[2]")

def eval_problem_160(response: str):
    return presence_eval(response, "[1]")

def eval_problem_161(response: str):
    return presence_eval(response, "[1]")

def eval_problem_162(response: str):
    return presence_eval(response, "[2]")

def eval_problem_163(response: str):
    return presence_eval(response, "[1]")

def eval_problem_164(response: str):
    return presence_eval(response, "[2]")

def eval_problem_165(response: str):
    return presence_eval(response, "[2]")

def eval_problem_166(response: str):
    return presence_eval(response, "[2]")

def eval_problem_167(response: str):
    return presence_eval(response, "[1]")

def eval_problem_168(response: str):
    return presence_eval(response, "[4]")

def eval_problem_169(response: str):
    return presence_eval(response, "[2]")

def eval_problem_170(response: str):
    return presence_eval(response, "[1]")

def eval_problem_171(response: str):
    return presence_eval(response, "[4]")

def eval_problem_172(response: str):
    return presence_eval(response, "[2]")

def eval_problem_173(response: str):
    return presence_eval(response, "[1]")

def eval_problem_174(response: str):
    return presence_eval(response, "[4]")

def eval_problem_175(response: str):
    return presence_eval(response, "[2]")

def eval_problem_176(response: str):
    return presence_eval(response, "[4]")

def eval_problem_177(response: str):
    return presence_eval(response, "[2]")

def eval_problem_178(response: str):
    return presence_eval(response, "[1]")

def eval_problem_179(response: str):
    return presence_eval(response, "[4]")

def eval_problem_180(response: str):
    return presence_eval(response, "[2]")

def eval_problem_181(response: str):
    return presence_eval(response, "[1]")

def eval_problem_182(response: str):
    return presence_eval(response, "[4]")

def eval_problem_183(response: str):
    return presence_eval(response, "[2]")

def eval_problem_184(response: str):
    return presence_eval(response, "[1]")

def eval_problem_185(response: str):
    return presence_eval(response, "[4]")

def eval_problem_186(response: str):
    return presence_eval(response, "[2]")

def eval_problem_187(response: str):
    return presence_eval(response, "[1]")

def eval_problem_188(response: str):
    return presence_eval(response, "[4]")

def eval_problem_189(response: str):
    return presence_eval(response, "[2]")

def eval_problem_190(response: str):
    return presence_eval(response, "[1]")

def eval_problem_191(response: str):
    return presence_eval(response, "[3]")

def eval_problem_192(response: str):
    return presence_eval(response, "[2]")

def eval_problem_193(response: str):
    return presence_eval(response, "[3]")

def eval_problem_194(response: str):
    return presence_eval(response, "[1]")

def eval_problem_195(response: str):
    return presence_eval(response, "[4]")

def eval_problem_196(response: str):
    return presence_eval(response, "[4]")

def eval_problem_197(response: str):
    return presence_eval(response, "[3]")

def eval_problem_198(response: str):
    return presence_eval(response, "[3]")

def eval_problem_199(response: str):
    return presence_eval(response, "[2]")

def eval_problem_200(response: str):
    return presence_eval(response, "[2]")

def eval_problem_201(response: str):
    return presence_eval(response, "[2]")
