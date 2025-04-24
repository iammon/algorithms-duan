"""
seam.py

Resize a P2-format PGM image by seam carving
- Part I: remove N vertical seams
- Part II: then remove M horizontal seams
"""

import numpy as np
import copy

# DO NOT modify this cell.
filename = "Buchtel.pgm"
verticalSeam2Remove = 10
horizontalSeam2Remove = 8

# Output filenames
filename1 = filename.split(".")[0] + "_processed_" + str(verticalSeam2Remove) + "_0.pgm"
print(filename1)

filename2 = filename.split(".")[0] + "_processed_" + \
            str(verticalSeam2Remove) + "_" + str(horizontalSeam2Remove) + ".pgm"
print(filename2)

# ---------- PGM I/O ----------
def read_pgm(fname):
    print(f"Reading image from file: {fname}")
    with open(fname, 'r') as f:
        magic = f.readline().strip()
        if magic != "P2":
            raise ValueError("Only P2-format (ASCII) PGM supported")
        line = f.readline()
        while line.startswith('#'):
            line = f.readline()
        width, height = map(int, line.split())
        max_gray = int(f.readline().strip())

        # Read all remaining pixels as a flat list
        data = []
        for line in f:
            if line.strip() == '':
                continue
            data.extend(map(int, line.strip().split()))
        
        if len(data) != width * height:
            raise ValueError(f"Expected {width * height} pixels, but got {len(data)}")

        pixels = [data[i * width:(i + 1) * width] for i in range(height)]

    print(f"Image loaded: {height} rows × {width} cols")
    return pixels, width, height, max_gray


def save_pgm(fname, img, max_gray):
    print(f"Saving image to file: {fname}")
    height = len(img)
    width = len(img[0])
    with open(fname, 'w') as f:
        f.write("P2\n")
        f.write(f"{width} {height}\n")
        f.write(f"{max_gray}\n")
        for row in img:
            f.write(" ".join(map(str, row)) + "\n")

# ---------- Energy Function ----------
def compute_energy(img):
    arr = np.array(img, dtype=int)
    print(f"Computing energy for shape: {arr.shape}")

    # Roll the image in all directions
    up    = np.roll(arr, 1, axis=0)
    down  = np.roll(arr, -1, axis=0)
    left  = np.roll(arr, 1, axis=1)
    right = np.roll(arr, -1, axis=1)

    # Avoid wrapping
    up[0, :] = arr[0, :]
    down[-1, :] = arr[-1, :]
    left[:, 0] = arr[:, 0]
    right[:, -1] = arr[:, -1]

    # Compute energy
    energy = np.abs(arr - up) + np.abs(arr - down) + np.abs(arr - left) + np.abs(arr - right)
    return energy

# ---------- Vertical Seam Functions ----------
def find_vertical_seam(energy):
    h, w = energy.shape
    cost = energy.copy()
    back = np.zeros_like(cost, dtype=int)

    for i in range(1, h):
        for j in range(w):
            min_cost, idx = cost[i-1, j], j
            if j > 0 and cost[i-1, j-1] < min_cost:
                min_cost, idx = cost[i-1, j-1], j-1
            if j < w-1 and cost[i-1, j+1] < min_cost:
                min_cost, idx = cost[i-1, j+1], j+1
            cost[i, j] += min_cost
            back[i, j] = idx

    seam = []
    j = int(np.argmin(cost[-1]))
    for i in range(h-1, -1, -1):
        seam.append((i, j))
        j = back[i, j]
    return list(reversed(seam))

def remove_vertical_seam(img, seam):
    return [row[:j] + row[j+1:] for row, (_, j) in zip(img, seam)]

def remove_n_vertical_seams(img, n):
    for i in range(n):
        print(f"[Vertical] Removing seam {i+1}/{n}")
        if len(img[0]) <= 1:
            print("Image too narrow for more vertical seams.")
            break
        energy = compute_energy(img)
        seam = find_vertical_seam(energy)
        img = remove_vertical_seam(img, seam)
    return img

# ---------- Horizontal Seam Functions ----------
def transpose(img):
    return [list(col) for col in zip(*img)]

def remove_n_horizontal_seams(img, n):
    img_t = transpose(img)
    for i in range(n):
        print(f"[Horizontal] Removing seam {i+1}/{n}")
        if len(img_t[0]) <= 1:
            print("Image too short for more horizontal seams.")
            break
        energy = compute_energy(img_t)
        seam = find_vertical_seam(energy)
        img_t = remove_vertical_seam(img_t, seam)
    return transpose(img_t)

# ---------- Main ----------
def main():
    print("Starting seam carving...")

    # Load image
    pixels, w, h, max_gray = read_pgm(filename)
    print(f"Original image size: {len(pixels)} rows × {len(pixels[0])} cols")

    # Part I — vertical seams only
    img_v = remove_n_vertical_seams(copy.deepcopy(pixels), verticalSeam2Remove)
    save_pgm(filename1, img_v, max_gray)

    # Part II — vertical + horizontal seams
    img_vh = remove_n_horizontal_seams(copy.deepcopy(img_v), horizontalSeam2Remove)
    save_pgm(filename2, img_vh, max_gray)

    print("Seam carving completed!")

if __name__ == "__main__":
    main()
