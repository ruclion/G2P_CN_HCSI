import databaker_G2P_1 as g2p_1
import pinyin_G2P_2 as g2p_2



def main():
    meta = g2p_1.build_from_path_CN('/ceph/home/hujk17/TTS.DataBaker.zhcmn.enus.F.DB6.emotion/CN/000001-010000.txt', use_prosody = True)
    finished = g2p_1.write_metadata(meta, 'databaker_MIX_Phoneme')
    print('tag:', finished)


    ans1 = g2p_2.pinyin_to_symbols('ma1 ma1 dang1 shi2 biao3 shi4 er2 zi5 kai1 xin1 de5 xiang4 huar1 yi2 yang4')
    ans2 = g2p_2.pinyin_to_symbols('ma1-ma1 dang1-shi2 biao3-shi4, er2-zi5 kai1-xin1-de5 / xiang4-huar1 yi2-yang4.')
    # TODO
    ans3 = g2p_2.pinyin_to_symbols('ma1-ma1 dang1-shi2 biao3-shi4, er2-zi5 kai1-xin1-de5 / xiang4-huar1 yi2-yang4?')
    print(ans1)
    print(ans2)
    print(ans3)


if __name__ == "__main__":
    main()


