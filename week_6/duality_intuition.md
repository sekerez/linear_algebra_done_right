
# Duality geometrical intuition

Consider the vector space $V$ and the basis $(v_1, v_2, \ldots, v_n)$ for $V$.

The concept of basis $(\varphi_1, \varphi_2, \ldots, \varphi_n)$ for the the dual space $V'$ is defined in ... in terms of the 1-0 properties: for $\varphi_i(v_j) = \delta_{ij}$, where $\delta_{ij}$ is the Diract delta function (1 when $i = j$, and 0 otherwise).

Axler leaves the $\varphi$s only defined abstractly, as functionals $\mathcal{L}(V,F)$, where $V$ is any abstract vector space.

If we restrict out attention to the case $V=\mathbb{R}^n$ (or $F^n$ if you prefer), then we can gain some valuable intuition about the nature of the $\varphi$s.

As Isak pointed out, we can think of the $\varphi$s as function of the form:
\[
  \varphi(v) = \vec{a} \cdot v,
\]
for some vector $\vec{a}$. In other words, each $\varphi_i$ corresponds to some vector $\vec{a}_i$ and applying $\varphi_i$ to vector $v$ is equivalent to computing the dot product $\vec{a}\cdot v$.

Geometrically speaking, the functions $\varphi_i$ compute the distance from a plane passing through the origin that has normal vector $\vec{a}_i$, up to a constant factor related to $\|\vec{a}_i\|$.



### Example 1: dual to the standard basis

Consider $V=\mathbb{R}^2$ and the standard basis for $V$ that consisting of
\[
    e_1 = (1,0)
    \quad \textrm{and}
    \quad
    e_2 = (0,1).
\]

The dual basis consists of the functionals
\[
    \varphi_1(v) = (1,0) \cdot v
    \quad \textrm{and}
    \quad
    \varphi_2(v) = (0,1) \cdot v,
\]
which manifestly satisfy the 1-0 proprty $\varphi_i(e_j) = \delta_{ij}$.



### Example 2: dual to non-orthogonal basis

Consider again $V=\mathbb{R}^2$ and the basis for $V$ that consisting of
\[
    v_1 = (2,0)
    \quad \textrm{and}
    \quad
    v_2 = (1,1).
\]

The dual basis consists of the functionals
\[
    \varphi_1(v) = (\tfrac{1}{2},-\tfrac{1}{2}) \cdot v
    \quad \textrm{and}
    \quad
    \varphi_2(v) = (0,1) \cdot v,
\]
which we can verify satisfies the 1-0 property $\varphi_i(v_j) = \delta_{ij}$.


Credit David for providing the algorithm for finding the vectors $\vec{a}_i$ needed to create the dual basis functionals $\varphi_i$. The algorith is:
1. stack vectors $e$s into matrix M
2. find inverse of M
3. read-off $a_i$s as the cols of M inverse

You can see SymPy code that implements the above steps for the vectors $v_1$ and $v_2$ [here](https://live.sympy.org/?evaluate=M%20%3D%20Matrix(%5B%5B2%2C0%5D%2C%5B1%2C1%5D%5D)%0A%23--%0AM%0A%23--%0AM.inv()%0A%23--%0AM.inv()%20*%20M%0A%23--%0A).






## Understanding dual representations geometrically

Recall we said that the elements of the dual basis $\phi_i$ can be interpreted geometrically as functions that compute the distance to the plane passing through the origin with normal vector $\vec{a}_i$, up a multiplier constant.

Let's revisit the two examples to see how this geometric intuition applies to them.

### Example 1

Every vector $v \in V$ can be represented as a linear combination of the basis vectors $e_1$ and $e_2$:
\[
    v = \alpha_1 e_1 + \alpha_2 e_2,
\]
where the coefficients $\alpha_i$ correspond to the "how much of $e_i$ is in $v$" calculations.

Equivalently, the same vector $v$ can be represented in terms of two coefficients $\beta_1$ and $\beta_2$ obtained by asking the questions "how far is $\vec{v}$ from the planes with normal vector $\vec{a}_1 =(1,0)$ and $\vec{a}_2 =(0,1)$."
\[
    \beta_1 = \varphi_1(v) = \vec{a}_1 \cdot v
    \quad \textrm{and}
    \quad
    \beta_2 = \varphi_2(v) = \vec{a}_2 \cdot v.
\]

In this case, since we're dealing with the an orthonormal basis $e_i$, which leads to self-dual vectors $\vec{a}_i$, the coefficients $\alpha_i$ and $\beta_i$ are the same.


### Example 2

Every vector $v \in V$ can be represented as a linear combination of the basis vectors $v_1$ and $v_2$:
\[
    v = \alpha_1 v_1 + \alpha_2 v_2,
\]
and we know that $\alpha_1$ and $\alpha_2$ are unique coefficients that make up the linear combination (since $v_1$ and $v_2$ are linearly independent). We can still interpret $\alpha_1$ and $\alpha_2$ as "how much of $v_i$ is needed to get $v$".


Equivalently, the same vector $v$ can be represented in terms of two coefficients $\beta_1$ and $\beta_2$ obtained by asking the questions "how far is $\vec{v}$ from the planes with normal vector $\vec{a}_1 = (\tfrac{1}{2},-\tfrac{1}{2})$ and $\vec{a}_2 = (0,1)$."
\[
    \beta_1 = \varphi_1(v) = \vec{a}_1 \cdot v
    \quad \textrm{and}
    \quad
    \beta_2 = \varphi_2(v) = \vec{a}_2 \cdot v.
\]

Caveat: the coefficients $\beta_i$ are not actually equal tot he distances from the plane $\phi_i$ as claimed above, but related by a constant. If we wanted a to have a representation in terms of actual, geometrical distances to the planes, we'd have to use the coefficients $\hat{\beta}_i$ defined as
\[
    \hat{\beta}_1 = \hat{a}_1 \cdot v
    \quad \textrm{and}
    \quad
    \hat{\beta}_2 = \hat{a}_2 \cdot v,
\]
where $\hat{a}_i = \frac{\vec{a}_i}{\|\vec{a}_i\|}$ are unit-length vectors in the same direction as $\vec{a}_i$.

Since the real geometrical distances $\hat{\beta}_i$ and the outputs of the functionals $\varphi_i$ are related by the constant $\|\vec{a}_i\|$ we allow ourselves to use "loose" language and refer to the coefficeints $\beta_i$ as distances,
but keep in mind actual distances are $\hat{\beta}_i = \beta_i/\|\vec{a}_i\|$.



## Graphs of functionals

Another way to think about the functionals $\varphi_1 : \mathbb{R}^2 \to \mathbb{R}$ and $\varphi_2 : \mathbb{R}^2 \to \mathbb{R}$ is in therms of their "graph" in $\mathbb{R}^3$.

The graph of the multivariable function $f : \mathbb{R}^2 \to \mathbb{R}$ consists of all points $(x,y,f(x,y))$ in $\mathbb{R}^3$, for all possible $(x,y) \in \mathbb{R}^2$. In the case of the functions $\varphi_1$ and $\varphi_2$, the graph are planes.

Isak pointed out the general notion that three points in $\mathbb{R}^3$ uniquely define a plane. He also observed that we can use the 1-0 property $\varphi_i(v_j) = \delta_{ij}$ to obtain the coordinates of three points for each $\varphi_i$,
and hence we can find them this way... (in particular this shows the dual basis $\varphi_1$ and $\varphi_2$ is unique).

Specifically, we know that:
- $\varphi_1(v_1) = 1$, $\varphi_1(v_2) = 0$, and $\varphi_1(0) = 0$
- $\varphi_2(v_1) = 0$, $\varphi_2(v_2) = 1$, and $\varphi_2(0) = 0$
The zero values tell us the graph of each $\varphi_i$ intersects $xy$-plane on some line. The plane that corresponds to $\varphi_1$ some "twist" along the line $0$ to $v_i$.
The value $\varphi_i(v_i) = 1$ tells us how much to twist...





