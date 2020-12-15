import pinyin as py_hcsi


def main():
    ans1 = py_hcsi.pinyin_to_symbols('ma1 ma1 dang1 shi2 biao3 shi4 er2 zi5 kai1 xin1 de5 xiang4 huar1 yi2 yang4')
    ans2 = py_hcsi.pinyin_to_symbols('ma1-ma1 dang1-shi2 biao3-shi4, er2-zi5 kai1-xin1-de5 / xiang4-huar1 yi2-yang4.')
    # TODO
    ans3 = py_hcsi.pinyin_to_symbols('ma1-ma1 dang1-shi2 biao3-shi4, er2-zi5 kai1-xin1-de5 / xiang4-huar1 yi2-yang4?')
    print(ans1)
    print(ans2)
    print(ans3)


if __name__ == "__main__":
    main()


