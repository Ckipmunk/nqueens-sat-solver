"""
Module: amo_encodings.py
Mục đích: Cài đặt và phân tích 5 kỹ thuật mã hóa At-Most-One (AMO):
1. Pairwise / Direct Encoding (PySAT CardEnc.pairwise hoặc tự cài đặt)
2. Sequential Counter Encoding (Sinz, 2005 - PySAT CardEnc.seqcounter hoặc tự cài đặt)
3. Commander Variable Encoding (Klieber & Kwon, 2007 - Tự cài đặt theo bài báo gốc)
4. Binary / Bitwise Encoding (Frisch et al., 2005 / PySAT CardEnc.bitwise)
5. Product Encoding (Chen, 2010 - Tự cài đặt theo bài báo gốc)

Ghi chú phân định rõ ràng giữa hàm gọi qua PySAT CardEnc và các hàm tự cài đặt.
"""

import math
from typing import List, Tuple

class VarManager:
    """Quản lý cấp phát biến logic mới cho SAT."""
    def __init__(self, start_id: int = 1):
        self.next_var = start_id

    def allocate(self, count: int = 1) -> List[int]:
        allocated = list(range(self.next_var, self.next_var + count))
        self.next_var += count
        return allocated

    def new_var(self) -> int:
        var = self.next_var
        self.next_var += 1
        return var


def encode_alo(literals: List[int]) -> List[List[int]]:
    """
    At-Least-One (ALO): Ít nhất một biến nhận giá trị True.
    Mệnh đề: (x_1 OR x_2 OR ... OR x_k)
    """
    if not literals:
        return []
    return [list(literals)]


# ==============================================================================
# 1. PAIRWISE / DIRECT ENCODING
# ==============================================================================
def encode_amo_pairwise(literals: List[int]) -> List[List[int]]:
    """
    1. Pairwise / Direct Encoding:
    Tạo mệnh đề (-x_i OR -x_j) với mọi 1 <= i < j <= k.
    - Số biến phụ: 0
    - Số mệnh đề: k * (k - 1) / 2 = O(k^2)
    (Có thể gọi qua PySAT CardEnc.atmost(literals, 1, encoding=EncType.pairwise))
    """
    clauses = []
    n = len(literals)
    for i in range(n):
        for j in range(i + 1, n):
            clauses.append([-literals[i], -literals[j]])
    return clauses


# ==============================================================================
# 2. SEQUENTIAL COUNTER ENCODING (Sinz, 2005)
# ==============================================================================
def encode_amo_sequential_counter(literals: List[int], var_mgr: VarManager) -> List[List[int]]:
    """
    2. Sequential Counter Encoding (Sinz, 2005):
    Sử dụng k-1 biến phụ s_1, s_2, ..., s_{k-1} làm thanh ghi tích lũy.
    - s_i là True nếu có ít nhất 1 biến trong x_1..x_i là True.
    - Số biến phụ: k - 1 = O(k)
    - Số mệnh đề: 3k - 4 = O(k)
    (Tương đương với PySAT CardEnc.atmost(literals, 1, encoding=EncType.seqcounter))
    """
    k = len(literals)
    if k <= 1:
        return []
    if k == 2:
        return [[-literals[0], -literals[1]]]

    s = var_mgr.allocate(k - 1)
    clauses = []

    # -x_1 OR s_1
    clauses.append([-literals[0], s[0]])

    for i in range(1, k - 1):
        x_curr = literals[i]
        s_prev = s[i - 1]
        s_curr = s[i]

        clauses.append([-x_curr, s_curr])
        clauses.append([-s_prev, s_curr])
        clauses.append([-x_curr, -s_prev])

    clauses.append([-literals[-1], -s[-1]])
    return clauses


# ==============================================================================
# 3. COMMANDER VARIABLE ENCODING (Klieber & Kwon, 2007)
# ==============================================================================
def encode_amo_commander(literals: List[int], var_mgr: VarManager, group_size: int = 3) -> List[List[int]]:
    """
    3. Commander Variable Encoding (Klieber & Kwon, 2007):
    [Tự cài đặt - Thư viện PySAT CardEnc chuẩn không tích hợp sẵn phương pháp này]
    Chia k biến thành các nhóm nhỏ kích thước <= group_size (mặc định 3).
    Mỗi nhóm có 1 biến chỉ huy c_g.
    - Trong mỗi nhóm: AMO(group)
    - Liên kết: (x_i -> c_g) <=> (-x_i OR c_g) và (c_g -> ALO(group))
    - Áp dụng đệ quy AMO lên tập các biến chỉ huy c_g.
    - Số biến phụ: O(k)
    - Số mệnh đề: O(k)
    """
    k = len(literals)
    if k <= 1:
        return []
    if k <= group_size:
        return encode_amo_pairwise(literals)

    groups = [literals[i:i + group_size] for i in range(0, k, group_size)]
    commanders = var_mgr.allocate(len(groups))
    clauses = []

    for g_idx, group in enumerate(groups):
        c = commanders[g_idx]

        # 1. AMO nội bộ nhóm (dùng pairwise vì group_size nhỏ = 3)
        clauses.extend(encode_amo_pairwise(group))

        # 2. Nếu bất kỳ x trong nhóm bật -> c phải bật
        for x in group:
            clauses.append([-x, c])

        # 3. Nếu c bật -> ít nhất 1 biến trong nhóm phải bật
        clauses.append([-c] + group)

    # 4. AMO đệ quy trên tập biến chỉ huy
    clauses.extend(encode_amo_commander(commanders, var_mgr, group_size))
    return clauses


# ==============================================================================
# 4. BINARY / BITWISE ENCODING (Frisch et al., 2005)
# ==============================================================================
def encode_amo_binary(literals: List[int], var_mgr: VarManager) -> List[List[int]]:
    """
    4. Binary / Bitwise Encoding (Frisch et al., 2005):
    Sử dụng m = ceil(log2(k)) biến phụ b_1..b_m mã hóa vị trí nhị phân.
    - Số biến phụ: ceil(log2(k)) = O(log k)
    - Số mệnh đề: k * ceil(log2(k)) = O(k log k)
    (Tương đương với PySAT CardEnc.atmost(literals, 1, encoding=EncType.bitwise))
    """
    k = len(literals)
    if k <= 1:
        return []
    if k == 2:
        return [[-literals[0], -literals[1]]]

    m = math.ceil(math.log2(k))
    bits = var_mgr.allocate(m)
    clauses = []

    for i, x in enumerate(literals):
        for j in range(m):
            bit_val = (i >> j) & 1
            b = bits[j]
            if bit_val == 1:
                clauses.append([-x, b])
            else:
                clauses.append([-x, -b])

    return clauses


# ==============================================================================
# 5. PRODUCT ENCODING (Chen, 2010)
# ==============================================================================
def encode_amo_product(literals: List[int], var_mgr: VarManager) -> List[List[int]]:
    """
    5. Product Encoding (Chen, 2010):
    [Tự cài đặt - Thư viện PySAT CardEnc chuẩn không tích hợp sẵn phương pháp này]
    Ánh xạ k biến thành ma trận 2D kích thước p x q sao cho p * q >= k.
    Chọn p = floor(sqrt(k)), q = ceil(k / p).
    - p biến phụ hàng u_1..u_p
    - q biến phụ cột v_1..v_q
    - Số biến phụ: p + q = O(sqrt(k))
    - Số mệnh đề: 2k + O(p^2 + q^2) = O(k)
    """
    k = len(literals)
    if k <= 1:
        return []
    if k <= 3:
        return encode_amo_pairwise(literals)

    p = int(math.isqrt(k))
    q = math.ceil(k / p)

    u_vars = var_mgr.allocate(p)
    v_vars = var_mgr.allocate(q)
    clauses = []

    clauses.extend(encode_amo_pairwise(u_vars))
    clauses.extend(encode_amo_pairwise(v_vars))

    for idx, x in enumerate(literals):
        r = idx // q
        c = idx % q
        u_r = u_vars[r]
        v_c = v_vars[c]

        clauses.append([-x, u_r])
        clauses.append([-x, v_c])

    return clauses


def encode_amo(literals: List[int], method: str, var_mgr: VarManager) -> List[List[int]]:
    """
    Dispatcher hàm mã hóa AMO theo phương pháp:
    - 'pairwise'
    - 'sequential' (Sinz, 2005)
    - 'commander' (Klieber & Kwon, 2007)
    - 'binary' (Frisch et al., 2005)
    - 'product' (Chen, 2010)
    """
    method = method.lower()
    if method in ('pairwise', 'direct'):
        return encode_amo_pairwise(literals)
    elif method in ('sequential', 'seq_counter', 'sinz'):
        return encode_amo_sequential_counter(literals, var_mgr)
    elif method in ('commander',):
        return encode_amo_commander(literals, var_mgr)
    elif method in ('binary', 'bitwise'):
        return encode_amo_binary(literals, var_mgr)
    elif method in ('product', '2d'):
        return encode_amo_product(literals, var_mgr)
    else:
        raise ValueError(f"Phương pháp mã hóa AMO không xác định: {method}")


def encode_exactly_one(literals: List[int], method: str, var_mgr: VarManager) -> List[List[int]]:
    """Exactly-One (EO) = ALO + AMO"""
    clauses = encode_alo(literals)
    clauses.extend(encode_amo(literals, method, var_mgr))
    return clauses
