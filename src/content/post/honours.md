---
layout: ../../layouts/post.astro
title: "Honours Thesis: The Face is the Soul of the Body"
description: 3D analysis of facial expressions
dateFormatted: Nov 30th, 2020
---

This post is about my Honours project. [View full thesis here](https://r2.lmor152.com/The%20Face%20is%20the%20Soul%20of%20the%20Body.pdf) or keep reading below for a summary.

# Introduction
The aim of this project was to use a stereoscope to capture images with high framerates and in HD. When used to film a face during various expressions, 3D point clouds can be created and deformations analysed to create efficient representations of faces.


# Stereoscope
We constructed a stereoscope using two FLIR Flea 3 cameras, a laser cut acrylic base, and a tripod. The two cameras were angled inwards carefully to optimise the captured area of the face infront of the cameras.

![pic](/assets/images/projects/honours/1.png)



# Matching
Before matching, the images have to be transformed to account for distortion. This ensures that all matching features will be in the same vertical coordinate. This means that the matching algorithms only need to search in the horizontal plane.
![pic](/assets/images/projects/honours/2.png)

Each individual pixel needs to be matched with its corresponding one in the neighbour image. This is done by using a group of pixels (centered around the target pixel), and finding the most similar group in the partner image. When this is completed, a depth for each pixel can be calculated.

# Point Clouds
After calculating a depth for each pixel in the photos, a raw 3D point cloud can be visualised:
![pic](/assets/images/projects/honours/3.png)

3D smoothing and some other post-processing techniques can be used to produce a refined point cloud:
![pic](/assets/images/projects/honours/4.png)

# Tracking
Applying 2D pixel tracking algorithms allows features of the face to be tracked through time, and the initial 3D point clouds can be shifted to match the expressions made in the photos:
![pic](/assets/images/projects/honours/5.png)


# Principal Component Analysis
Finally, PCA can be performed to determine the dominant modes of deformation. The first four principle components demonstrate face-like appearances:
![pic](/assets/images/projects/honours/6.png)


