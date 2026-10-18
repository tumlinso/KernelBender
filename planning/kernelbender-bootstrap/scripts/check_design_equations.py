#!/usr/bin/env python3
"""Finite CPU checks of illustrative design identities; no GPU or model evaluation."""
from __future__ import annotations
import itertools
import json
import random
import struct


def transpose(a): return list(map(list, zip(*a)))
def mm(a, b): return [[sum(x*y for x,y in zip(row,col)) for col in transpose(b)] for row in a]
def threshold_planes(masks: list[int], threshold: int, width: int) -> int:
    valid = (1 << width) - 1
    if threshold <= 0: return valid
    if threshold > len(masks): return 0
    planes: list[int] = []
    for mask in masks:
        carry, level = mask & valid, 0
        while carry:
            if level == len(planes): planes.append(0)
            old = planes[level]
            planes[level] = old ^ carry
            carry = old & carry
            level += 1
    greater, equal = 0, valid
    for bit in reversed(range(max(len(planes), threshold.bit_length()))):
        p = planes[bit] if bit < len(planes) else 0
        if (threshold >> bit) & 1:
            equal &= p
        else:
            greater |= equal & p
            equal &= ~p & valid
    return (greater | equal) & valid


def main() -> None:
    rng=random.Random(701810)
    groups=[]
    for a,b,c in itertools.product((0,1), repeat=3):
        s=a^b^c; carry=(a&b)|(a&c)|(b&c)
        assert a+b+c == s+2*carry
    groups.append({'name':'per-position full-adder identity','cases':8,'result':'passed'})
    count=0
    for width in (1,7,31,32,33):
        for n in (0,1,2,3,5,17):
            masks=[rng.getrandbits(width+2) for _ in range(n)]
            for t in range(n+2):
                expected=sum((sum((m>>i)&1 for m in masks)>=t)<<i for i in range(width))
                assert threshold_planes(masks,t,width)==expected
                count+=1
    groups.append({'name':'bitplane threshold preserves per-position multiplicity and tails','cases':count,'result':'passed','limit':'Symbolic integer-word CPU behavior, not warp mapping or GPU throughput'})
    for _ in range(40):
        x=[[rng.randint(-3,3) for _ in range(3)] for _ in range(2)]
        w=[[rng.randint(-3,3) for _ in range(5)] for _ in range(3)]
        v=[[rng.randint(-3,3) for _ in range(2)] for _ in range(5)]
        assert mm(mm(x,w),v)==mm(x,mm(w,v))
        h=mm(x,w); gram=mm(w,transpose(w))
        for row,response in zip(x,h):
            assert sum(a*a for a in response)==mm(mm([row],gram),[[q] for q in row])[0][0]
    groups.append({'name':'linear consumer reassociation and quadratic observable identity','cases':80,'result':'passed','limit':'Exact bounded integer algebra; no claim of identical finite-precision evaluation'})
    half=lambda x:struct.unpack('e',struct.pack('e',x))[0]
    f32=lambda x:struct.unpack('f',struct.pack('f',x))[0]
    a,b,c=half(1.001),half(1.001),half(1000)
    staged=f32(half(a*b)*c)
    reassociated=f32(a*half(b*c))
    assert staged != reassociated
    groups.append({'name':'required intermediate rounding defeats naive reassociation','cases':1,'result':'counterexample confirmed','represented_inputs':[a,b,c],'staged':staged,'reassociated':reassociated,'limit':'Explicit CPU IEEE formats, not proprietary Tensor Core arithmetic'})
    for _ in range(40):
        a1=[[rng.randint(-2,2) for _ in range(2)] for _ in range(2)]
        a2=[[rng.randint(-2,2) for _ in range(2)] for _ in range(2)]
        b1=[[rng.randint(-2,2)] for _ in range(2)]
        b2=[[rng.randint(-2,2)] for _ in range(2)]
        x=[[rng.randint(-2,2)] for _ in range(2)]
        add=lambda p,q:[[u[0]+v[0]] for u,v in zip(p,q)]
        assert add(mm(a2,add(mm(a1,x),b1)),b2)==add(mm(mm(a2,a1),x),add(mm(a2,b1),b2))
    groups.append({'name':'chronological affine-summary composition','cases':40,'result':'passed','limit':'Only the stated affine operator with available inputs'})
    values=[1,2,3,4]; perm=[0,2,1,3]
    f=lambda x:x*x+2*x
    assert [f(values[i]) for i in perm]==[f(x) for x in [values[i] for i in perm]]
    assert [sum(values[:2]),sum(values[2:])] != [values[0]+values[2],values[1]+values[3]]
    groups.append({'name':'permutation-compatible elementwise work versus changed reduction axes','cases':2,'result':'passed'})
    print(json.dumps({'status':'passed','groups':groups,'limits':['Finite CPU algebra/counterexample checks only.','No native kernel compilation, GPU profiling, model trial or skill-effectiveness claim.']},indent=2))

if __name__=='__main__': main()
