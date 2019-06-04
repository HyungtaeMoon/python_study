def insertion_sort(a):
    for i in range(1, len(a)):
        for j in range(i, 0, -1):
            # j 의 역순으로 순회하여 j 값과 그 앞의 값을 비교
            print(j)
            if a[j-1] > a[j]:
                a[j], a[j-1] = a[j-1], a[j]
        print(f'\t 정렬 과정: {a}')
    print(f'정렬 결과: {a}')


if __name__ == "__main__":
    a = [54, 88, 77, 26, 93, 17, 49, 10, 77, 11]
    insertion_sort(a)
    print(a)
