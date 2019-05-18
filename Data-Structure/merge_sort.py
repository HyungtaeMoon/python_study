def merge(a, b, low, mid, high):
    i = low
    j = mid + 1
    for k in range(low, high + 1):  # a의 앞/뒷부분을 합병하여 b에 저장
        if i > mid:
            b[k] = a[j]  # 앞부분이 먼저 소진된 경우
            j += 1
        elif j > high:
            b[k] = a[i]  # 뒷부분이 먼저 소진된 경우
            i += 1
        elif a[j] < a[i]:
            b[k] = a[j]  # a[j]가 승자(a[j] 값이 더 작음)
            j += 1
        else:
            b[k] = a[i]  # a[i]가 승자
            i += 1
    for k in range(low, high + 1):
        a[k] = b[k]  # b를 a에 복사


def merge_sort(a, b, low, high):
    if high <= low:
        return
    mid = low + (high - low) // 2
    merge_sort(a, b, low, mid)  # 앞부분 재귀호출
    merge_sort(a, b, mid + 1, high)  # 뒷부분 재귀호출
    merge(a, b, low, mid, high)  # 합병 수행


if __name__=='__main__':
    # a = [54, 88, 77, 26, 93, 17, 49, 10, 17, 77, 11, 31, 22, 44, 17, 20]
    a = [80, 40, 50, 10, 70, 20, 30, 60]
    b = [None] * len(a)
    print('정렬 전:\t', end='')
    print(a)
    merge_sort(a, b, 0, len(a) - 1)
    print('정렬 후 :\t', end='')
    print(a)