# Affine Transformation Analysis of Biped 2D Keypoints

This repository contains code for analyzing and visualizing affine transformations between 2D keypoints of a biped model. The following mathematical overview outlines the key concepts and computations implemented in the code.

## Mathematical Overview

### 1. Affine Transformation

An **affine transformation** maps points from one coordinate system to another using a combination of linear transformations (such as rotation, scaling, and shear) and translation. In this analysis, the affine transformation is estimated to map keypoints from frame **P** to frame **Q**.

Given a set of corresponding points $$\( \mathbf{P} = \{\mathbf{p}_1, \mathbf{p}_2, \dots, \mathbf{p}_n\} \)$$ in frame **P** and $$\( \mathbf{Q} = \{\mathbf{q}_1, \mathbf{q}_2, \dots, \mathbf{q}_n\} \)$$ in frame **Q**, the affine transformation matrix $$\( \mathbf{M} \)$$ is a $$\( 2 \times 3 \)$$ matrix that satisfies:

$$\mathbf{q}_i = \mathbf{M} \cdot \mathbf{p}_i \quad \forall i = 1, 2, \dots, n$$

Where:
- $$\( \mathbf{p}_i = \begin{bmatrix} x_i^{(P)} \\ y_i^{(P)} \end{bmatrix} \)$$ is a point in frame **P**.
  
- $$\( \mathbf{q}_i = \begin{bmatrix} x_i^{(Q)} \\ y_i^{(Q)} \end{bmatrix} \)$$ is the corresponding point in frame **Q**.
  
- $$\( \mathbf{M} = \begin{bmatrix} m_{11} & m_{12} & t_x \\ m_{21} & m_{22} & t_y \end{bmatrix} \)$$ is the affine transformation matrix comprising rotation, scaling, and translation components.

### 2. Estimation of the Affine Transformation Matrix

The affine transformation matrix $$\( \mathbf{M} \)$$ is estimated using the **Least Squares** method, which minimizes the sum of squared residuals between the transformed points and the target points.

$$
\mathbf{M} = \underset{\mathbf{M}}{\arg\min} \sum_{i=1}^{n} \left\| \mathbf{q}_i - \mathbf{M} \cdot \mathbf{p}_i \right\|^2
$$

This optimization problem is solved using OpenCV's `estimateAffinePartial2D` function, which computes $$\( \mathbf{M} \)$$ that best aligns $$\( \mathbf{P} \)$$ to $$\( \mathbf{Q} \)$$.

### 3. Decomposition of the Affine Transformation Matrix

Once the affine matrix $$\( \mathbf{M} \)$$ is obtained, it can be decomposed into **rotation**, **scaling**, and **translation** components.

#### a. Affine Matrix Structure

$$
\mathbf{M} = \begin{bmatrix} \mathbf{A} & \mathbf{t} \end{bmatrix} = \begin{bmatrix} m_{11} & m_{12} & t_x \\ m_{21} & m_{22} & t_y \end{bmatrix}
$$

Where:
- $$\( \mathbf{A} = \begin{bmatrix} m_{11} & m_{12} \\ m_{21} & m_{22} \end{bmatrix} \)$$ is the linear transformation matrix.
  
- $$\( \mathbf{t} = \begin{bmatrix} t_x \\ t_y \end{bmatrix} \)$$ is the translation vector.

#### b. Singular Value Decomposition (SVD)

To separate rotation and scaling, perform Singular Value Decomposition on \( \mathbf{A} \):

$$
\mathbf{A} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T
$$

Where:
- $$\( \mathbf{U} \) and \( \mathbf{V} \)$$ are orthogonal matrices.
- $$\( \mathbf{\Sigma} = \begin{bmatrix} \sigma_1 & 0 \\ 0 & \sigma_2 \end{bmatrix} \)$$ contains the singular values representing scaling factors.

#### c. Rotation Matrix

The rotation matrix $$\( \mathbf{R} \)$$ is obtained by:

$$
\mathbf{R} = \mathbf{U} \mathbf{V}^T
$$

To ensure a proper rotation (i.e., $$\( \det(\mathbf{R}) = 1 \))$$, adjust $$\( \mathbf{U} \)$$ or $$\( \mathbf{V} \)$$ if necessary.

#### d. Scaling Factors

The scaling factors along the principal axes are given by the singular values:

$$
\mathbf{S} = \mathbf{\Sigma} = \begin{bmatrix} \sigma_1 & 0 \\ 0 & \sigma_2 \end{bmatrix}
$$

#### e. Translation Vector

The translation component $$\( \mathbf{t} \)$$ is directly taken from the affine matrix:

$$
\mathbf{t} = \begin{bmatrix} t_x \\ t_y \end{bmatrix}
$$

### 4. Rotation Angle Calculation

The rotation angle $$\( \theta \)$$ extracted from the rotation matrix $$\( \mathbf{R} \)$$ can be computed as:

$$
\theta = \arctan\left(\frac{r_{21}}{r_{11}}\right) = \arctan\left(\frac{m_{21}}{m_{11}}\right)
$$

Where:
- $$\( r_{11} \) and \( r_{21} \)$$ are elements of the rotation matrix $$\( \mathbf{R} \)$$.

To convert the angle from radians to degrees:

$$
\theta_{\text{deg}} = \theta \times \left( \frac{180}{\pi} \right)
$$

### 5. Applying the Affine Transformation

To transform a set of points $$\( \mathbf{P} \)$$ using the affine matrix $$\( \mathbf{M} \)$$, use homogeneous coordinates:

$$
\mathbf{p}_i' = \mathbf{M} \cdot \begin{bmatrix} x_i^{(P)} \\ y_i^{(P)} \\ 1 \end{bmatrix} = \begin{bmatrix} m_{11}x_i^{(P)} + m_{12}y_i^{(P)} + t_x \\ m_{21}x_i^{(P)} + m_{22}y_i^{(P)} + t_y \end{bmatrix}
$$

Where $$\( \mathbf{p}_i' \)$$ is the transformed point in frame **Q**.

### 6. Residuals and Mean Squared Error (MSE)

After applying the affine transformation, compute the residuals between the transformed points $$\( \mathbf{P}' \)$$ and the target points $$\( \mathbf{Q} \)$$:

$$
\text{Residual}_i = \mathbf{q}_i - \mathbf{p}_i'
$$

The **Mean Squared Error (MSE)** is then calculated as:

$$\(\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} \left\| \text{Residual}_i \right\|^2 = \frac{1}{n} \sum_{i=1}^{n} \left( (x_i^{(Q)} - x_i')^2 +(y_i^{(Q)} - y_i')^2 \right) \)$$

Where:
- $$\( n \)$$ is the number of corresponding keypoints.
- $$\( (x_i^{(Q)}, y_i^{(Q)}) \)$$ are the coordinates of the target point in frame **Q**.
- $$\( (x_i', y_i') \)$$ are the coordinates of the transformed point from frame **P**.

### 7. Summary of Variables in the Code

To correlate the mathematical formulas with your code:

| **Mathematical Symbol** | **Code Variable**          | **Description**                                     |
|-------------------------|----------------------------|-----------------------------------------------------|
| $$\( \mathbf{P} \)$$        | `pts_P`                    | NumPy array of points from frame P                  |
| $$\( \mathbf{Q} \)$$        | `pts_Q`                    | NumPy array of points from frame Q                  |
| $$\( \mathbf{M} \)$$       | `affine_matrix`            | Estimated affine transformation matrix              |
| $$\( \mathbf{R} \)$$       | `R`                        | Rotation matrix                                     |
| $$\( \mathbf{t} \)$$        | `t`                        | Translation vector                                  |
| $$\( \mathbf{S} \)$$        | `scales`                   | Scaling factors                                     |
| $$\( \text{Residual}_i \)$$| `residuals`                | Residuals between transformed and target points     |
| $$\( \text{MSE} \)$$        | `mse`                      | Mean Squared Error of the transformation            |

---

By understanding these mathematical concepts, you can gain deeper insights into how the affine transformation is estimated, decomposed, and applied to the 2D keypoints of the biped model. This foundation is crucial for interpreting the results and ensuring the accuracy of the transformation.
