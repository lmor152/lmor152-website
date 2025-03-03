---
layout: ../../layouts/post.astro
title: "Honours Thesis: The Face is the Soul of the Body"
description: 3D analysis of facial expressions
dateFormatted: Nov 30th, 2020
---

This post is about my Honours project, which was making and analysing point clouds from my face like the one below. 

<div class="sketchfab-embed-wrapper" style="display: flex; justify-content: center; align-items: center; margin: 20px 0; width: 100%;"> 
    <iframe frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/b4b064108ebf45bdb752c57fee155610/embed" width="800" height="600" style="width: 100%;">
    </iframe> 
</div>

You can download my thesis [here](https://r2.lmor152.com/The%20Face%20is%20the%20Soul%20of%20the%20Body.pdf) or keep reading here for a summary.




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


