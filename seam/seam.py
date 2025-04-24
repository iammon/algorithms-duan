"""

seam.py

Resize a P2-format PGM image by seam curving
- Part I: remove N vertical seams
- Part II: then remove M horizontal seams

"""

import sys
import numpy as np

# DO NOT modify this cell. 
filename = "Buchtel.pgm"
verticalSeam2Remove = 10
horizontalSeam2Remove = 8

# Yes, you can create your own test cases and you should. Do it in a new cell.

# Part I : Vertical seam removal only
# Save your processed file to img_processed_v_h.pgm
filename1 = filename.split(".")[0]+"_processed_"+str(verticalSeam2Remove)+"_0.pgm"
print(filename1)

# your code, add cells as you need

# Part II : both vertical and horizontal seams removal 
# Save your processed file to img_processed_v_h.pgm
filename2 = filename.split(".")[0]+"_processed_"+ \
            str(verticalSeam2Remove)+"_"+str(horizontalSeam2Remove)+".pgm"
print(filename2)

# your code, add cells as you need

# PGM I/O
def read_pgm(fname):
    """Read an ASCII P2 PGM file into a 2D list of ints."""
    with open(fname, 'r') as f:
        magic = f.readline().strip()
        if magic != "P2":
            raise ValueError("Only P2-format (ASCII) PGM supported")
        # skip comments
        line = f.readline()
        while line.startswith('#'):
            line = f.readline()
        width, height = map(int, line.split())
        max_gray = int(f.readline().strip())
        pixels = []
        for _ in range(height):
            row = []
            while len(row) < width:
                row.extend(map(int, f.readline().split()))
            pixels.append(row)
    return pixels, width, height, max_gray

def save_pgm(fname, img, max_gray):
    """Save a 2D list 'img' as an ASCII P2 PGM file."""
    height = len(img)
    width  = len(img[0])
    with open(fname, 'w') as f:
        f.write("P2\n")
        f.write(f"{width} {height}\n")
        f.write(f"{max_gray}\n")
        for row in img:
            f.write(" ".join(map(str, row)) + "\n")

# Energy calculations
def compute_energy(img):
    """
    Compute energy map using 4-neighbor gradient:
      e(i,j) = |v - up| + |v - down| + |v - left| + |v - right|
    Boundaries use zero-gradient outside.
    """
    arr = np.array(img, dtype=int)
    h, w = arr.shape
    energy = np.zeros((h, w), dtype=int)
    for i in range(h):
        for j in range(w):
            v     = arr[i, j]
            up    = arr[i-1, j] if i > 0   else v
            down  = arr[i+1, j] if i < h-1 else v
            left  = arr[i, j-1] if j > 0   else v
            right = arr[i, j+1] if j < w-1 else v
            energy[i, j] = abs(v - up) + abs(v - down) + abs(v - left) + abs(v - right)
    return energy

# Seam Finding & Removal (Vertical)
def find_vertical_seam(energy):
    """
    Dynamic-programming to find the minimal-energy vertical seam.
    Returns list of (row, col) from top→bottom. Ties break to leftmost.
    """
    h, w = energy.shape
    cost = energy.copy()
    back = np.zeros_like(cost, dtype=int)

    # Build cumulative cost table
    for i in range(1, h):
        for j in range(w):
            # candidates: up-left, up, up-right
            min_cost, idx = cost[i-1, j], j
            if j > 0 and cost[i-1, j-1] < min_cost:
                min_cost, idx = cost[i-1, j-1], j-1
            if j < w-1 and cost[i-1, j+1] < min_cost:
                min_cost, idx = cost[i-1, j+1], j+1
            cost[i, j] += min_cost
            back[i, j] = idx

    # Backtrack from bottom row
    seam = []
    j = int(np.argmin(cost[-1]))
    for i in range(h-1, -1, -1):
        seam.append((i, j))
        j = back[i, j]
    return list(reversed(seam))

def remove_vertical_seam(img, seam):
    """
    Remove a single vertical seam from 'img' given by seam coordinates.
    Returns the new image (width reduced by 1).
    """
    new_img = []
    for i, row in enumerate(img):
        j = seam[i][1]
        new_img.append(row[:j] + row[j+1:])
    return new_img

def remove_n_vertical_seams(img, n):
    """
    Remove 'n' vertical seams in sequence.
    """
    for _ in range(n):
        energy = compute_energy(img)
        seam   = find_vertical_seam(energy)
        img    = remove_vertical_seam(img, seam)
    return img

# Seam Removal (Horizontal via Transpose Trick)
def transpose(img):
    """Transpose a 2D list (rows↔columns)."""
    return [list(col) for col in zip(*img)]

def remove_n_horizontal_seams(img, n):
    """
    Remove 'n' horizontal seams by:
      1. Transpose → vertical seam removal
      2. Transpose back
    """
    t = transpose(img)
    t = remove_n_vertical_seams(t, n)
    return transpose(t)

# Main
# Read original image
pixels, w, h, max_gray = read_pgm(filename)

# Part I: Vertical seams only
img_v = remove_n_vertical_seams(pixels, verticalSeam2Remove)
save_pgm(filename1, img_v, max_gray)

# Part II: Vertical then Horizontal seams
# reload original to avoid cascading
pixels, _, _, _ = read_pgm(filename)
img_v = remove_n_vertical_seams(pixels, verticalSeam2Remove)
img_vh = remove_n_horizontal_seams(img_v, horizontalSeam2Remove)
save_pgm(filename2, img_vh, max_gray)