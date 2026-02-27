# Pricing Under Discontinuous Supply and Capacity Constraints: Excess Demand, Rationing, and Equilibrium Formation

## Abstract

This paper analyzes optimal pricing and equilibrium formation in a market where a producer faces a sharply discontinuous supply constraint: output can be produced at zero marginal cost up to a fixed capacity, beyond which marginal cost is infinite. Such environments arise naturally in capacity-limited industries such as electricity generation, telecommunications bandwidth, transportation slots, and event ticketing. Using a stylized but analytically rich demand system with strategic interdependence—where each consumer’s demand depends on price and aggregate demand—we develop a formal framework for producer pricing, equilibrium quantity determination, and the emergence of excess demand. We show that the producer optimally sets price by equating constrained supply to aggregate demand rather than marginal revenue to marginal cost, leading generically to equilibria with rationing. Comparative statics illustrate how excess demand responds to changes in capacity, market size, and demand externalities. The analysis highlights welfare distortions and allocation issues inherent in capacity-constrained markets and clarifies the economic logic behind non-price rationing mechanisms commonly observed in practice.

---

# 1. Introduction

Standard microeconomic theory of price determination typically assumes smooth cost functions and continuous supply responses. Under such assumptions, competitive or monopolistic equilibria are characterized by equalization of marginal cost and marginal revenue (or marginal willingness to pay), yielding prices that clear markets without rationing. However, many real-world markets violate these assumptions. Production technologies may exhibit hard capacity limits: beyond a certain output level, production is infeasible or prohibitively costly. Examples include electricity generation with fixed plant capacity, airline seats on a flight, broadband bandwidth during peak hours, and tickets for live events.

In these environments, supply is discontinuous. Up to capacity, marginal cost may be low or even zero, while beyond capacity marginal cost becomes effectively infinite. The resulting equilibrium concept differs fundamentally from the textbook case. Prices need not clear markets; instead, excess demand and rationing emerge endogenously. The producer’s pricing problem becomes one of choosing a price that maximizes profit subject to a quantity constraint, rather than choosing a quantity where marginal revenue equals marginal cost.

This paper provides a detailed theoretical analysis of such a setting using a concrete case study. A monopolistic producer can supply at most 10 units of a good at zero marginal cost. The market consists of 100 consumers, each with a demand function that depends on price and total market demand. This functional form introduces strategic interdependence: consumers’ demands are not independent but respond positively and negatively to aggregate consumption, capturing network effects or congestion-like feedbacks.

The goals of the paper are fourfold. First, we formally derive aggregate demand and the inverse demand curve implied by the individual demand system. Second, we construct the producer’s profit maximization problem under a binding capacity constraint and characterize the equilibrium price and quantity. Third, we analyze how excess demand arises at equilibrium and discuss rationing mechanisms. Fourth, we explore comparative statics and economic interpretation, connecting the model to real-world capacity-constrained markets and welfare considerations.

The analysis builds on established theories of monopoly pricing, capacity constraints, and rationing [1][2][3], while emphasizing the role of discontinuous cost structures in shaping equilibrium outcomes.

---

# 2. Model Environment

## 2.1 Market Structure

We consider a single producer (monopolist) supplying a homogeneous good to a finite set of consumers. The producer faces the following cost structure:

* For output ( Q \leq \bar{Q} = 10 ), total cost ( C(Q) = 0 ).
* For output ( Q > \bar{Q} ), marginal cost is infinite, making production infeasible.

Thus, the feasible production set is ( Q \in [0,10] ), with a perfectly flat cost up to capacity and a vertical supply curve at ( Q = 10 ).

The market consists of ( N = 100 ) consumers indexed by ( i = 1, \dots, 100 ).

## 2.2 Individual Demand with Strategic Interdependence

Each consumer has an individual demand function:

[
q_i = 400 - 100P + \frac{Q}{100} + 3Q^2 - \frac{Q^3}{20},
]

where:

* ( P ) is the market price,
* ( Q = \sum_{i=1}^{100} q_i ) is total market demand.

This demand system departs from standard separable preferences in that each individual’s demand depends explicitly on aggregate demand. Such dependence can capture:

* Positive network effects (the ( Q ) and ( Q^2 ) terms),
* Negative congestion or saturation effects (the ( -Q^3/20 ) term).

Strategic interdependence of this kind is well studied in models of consumption externalities and social interactions [4][5].

---

# 3. Aggregate Demand and Inverse Demand

## 3.1 Aggregation

Summing individual demands across all consumers yields:

[
Q = \sum_{i=1}^{100} q_i = 100 \left( 400 - 100P + \frac{Q}{100} + 3Q^2 - \frac{Q^3}{20} \right).
]

Simplifying:

[
Q = 40{,}000 - 10{,}000P + Q + 300Q^2 - 5Q^3.
]

Subtracting ( Q ) from both sides:

[
0 = 40{,}000 - 10{,}000P + 300Q^2 - 5Q^3.
]

Rearranging:

[
10{,}000P = 40{,}000 + 300Q^2 - 5Q^3.
]

## 3.2 Inverse Demand

The inverse demand function is therefore:

[
P(Q) = 4 + 0.03Q^2 - 0.0005Q^3.
]

This inverse demand curve is nonlinear and non-monotonic in general. For small ( Q ), price increases with ( Q ) due to positive externalities; for large ( Q ), the cubic term dominates and price declines, reflecting congestion or diminishing marginal willingness to pay. Such shapes are consistent with models of network goods with saturation [6].

---

# 4. Producer’s Profit Maximization Under Capacity Constraint

## 4.1 Profit Function

The producer chooses a price ( P ) to maximize profit:

[
\pi(P) = P \cdot \min{Q(P), \bar{Q}},
]

where ( Q(P) ) is the quantity demanded at price ( P ) and ( \bar{Q} = 10 ).

Given zero marginal cost up to capacity, profit is simply revenue.

## 4.2 Unconstrained Monopoly Benchmark

Absent the capacity constraint, the monopolist would choose ( Q ) to maximize:

[
\pi(Q) = P(Q) \cdot Q.
]

Using the inverse demand:

[
\pi(Q) = \left(4 + 0.03Q^2 - 0.0005Q^3\right)Q.
]

The first-order condition equates marginal revenue to zero marginal cost. However, the solution to this unconstrained problem generally yields ( Q^* > 10 ), reflecting strong demand at low cost.

## 4.3 Binding Capacity Constraint

Because the producer cannot supply more than 10 units, the relevant problem becomes:

[
\max_{P} ; \pi = P \cdot 10
\quad \text{subject to} \quad Q(P) \geq 10.
]

Equivalently, the producer sets the highest price ( P ) such that quantity demanded is at least 10. Using the inverse demand, the equilibrium price is:

[
P^* = P(10) = 4 + 0.03(10)^2 - 0.0005(10)^3 = 4 + 3 - 0.5 = 6.5.
]

Thus, the producer supplies ( Q = 10 ) units at price ( P = 6.5 ).

---

# 5. Excess Demand and Rationing

## 5.1 Excess Demand at Equilibrium

At price ( P = 6.5 ), aggregate demand equals 10 by construction. However, individual demands evaluated at this price may sum to more than 10 if consumers do not internalize the capacity constraint. In decentralized settings, each consumer treats ( P ) as given and demands ( q_i(P,Q) ), potentially generating notional demand exceeding capacity.

This mismatch is the essence of excess demand: at the posted price, desired consumption exceeds feasible supply [2].

## 5.2 Rationing Mechanisms

When excess demand arises, allocation must be resolved through non-price mechanisms. Common rationing schemes include:

* **Proportional rationing**: each consumer receives a fraction of their desired demand.
* **First-come, first-served**: early buyers obtain the good until capacity is exhausted.
* **Queuing or waiting time**: consumers incur time costs instead of paying higher prices.
* **Lotteries or priority rules**: allocation based on exogenous criteria.

Economic theory shows that such rationing schemes affect welfare and can distort incentives, sometimes leading to inefficiencies relative to price-clearing equilibria [7][8].

---

# 6. Comparative Statics

## 6.1 Capacity Changes

An increase in capacity ( \bar{Q} ) shifts the supply constraint outward. The equilibrium price becomes ( P(\bar{Q}) ), which may rise or fall depending on the shape of inverse demand. In this model, for moderate increases in ( Q ), positive demand externalities may raise price, while for large ( Q ), congestion effects reduce price.

## 6.2 Number of Consumers

Increasing the number of consumers ( N ) scales up aggregate demand and strengthens strategic interdependence. Holding capacity fixed, a larger market intensifies excess demand and increases equilibrium price, exacerbating rationing.

## 6.3 Strength of Demand Externalities

Changes in the coefficients on ( Q^2 ) and ( Q^3 ) alter the curvature of inverse demand. Stronger positive externalities increase willingness to pay at higher quantities, raising scarcity rents. Stronger negative externalities dampen demand and can reduce excess demand even under tight capacity.

---

# 7. Economic Interpretation and Real-World Applications

## 7.1 Capacity-Constrained Industries

The model captures key features of several industries:

* **Electricity markets**: generation capacity is fixed in the short run; during peak demand, prices spike and blackouts or rolling rationing occur [9].
* **Telecommunications**: bandwidth constraints lead to congestion pricing or throttling [10].
* **Event ticketing**: venues have fixed seating capacity; excess demand leads to queues, lotteries, or resale markets [11].

In all cases, discontinuous supply induces scarcity rents and non-price allocation.

## 7.2 Welfare Implications

While capacity pricing maximizes producer profit, it may not maximize social welfare. Rationing can waste resources (e.g., time spent queuing) and allocate goods inefficiently. Policy interventions—such as capacity expansion, peak-load pricing, or secondary markets—aim to mitigate these losses [3][12].

---

# 8. Conclusion

This paper has shown how discontinuous supply constraints fundamentally alter price determination and equilibrium outcomes. When marginal cost jumps from zero to infinity at a fixed capacity, the producer optimally sets price to extract scarcity rents, leading generically to equilibria with excess demand and rationing. Using a demand system with strategic interdependence, we illustrated how aggregate demand, pricing, and welfare depend on capacity, market size, and externalities.

The analysis underscores that in capacity-limited markets, prices need not clear markets, and allocation mechanisms outside the price system play a central role. Understanding these dynamics is essential for both economic theory and policy design in industries where capacity constraints are unavoidable.

---

## References

[1] Tirole, J. The Theory of Industrial Organization – https://mitpress.mit.edu/9780262700461/
[2] Varian, H. R. Microeconomic Analysis – https://wwnorton.com/books/9780393123991
[3] Mas-Colell, A., Whinston, M. D., & Green, J. R. Microeconomic Theory – https://global.oup.com/academic/product/microeconomic-theory-9780195073409
[4] Katz, M. L., & Shapiro, C. “Network Externalities, Competition, and Compatibility.” American Economic Review – https://www.aeaweb.org/articles?id=10.1257/aer.75.3.424
[5] Glaeser, E. L., & Scheinkman, J. A. “Measuring Social Interactions.” Handbook of Social Economics – https://www.sciencedirect.com/science/article/pii/S1574008009000059
[6] Farrell, J., & Klemperer, P. “Coordination and Lock-In.” Handbook of Industrial Organization – https://www.sciencedirect.com/science/article/pii/S157344280600031X
[7] Benassy, J.-P. The Economics of Market Disequilibrium – https://www.elsevier.com/books/the-economics-of-market-disequilibrium/benassy/9780120929501
[8] Barzel, Y. “Queueing and the Allocation of Goods.” Journal of Political Economy – https://www.journals.uchicago.edu/doi/10.1086/259600
[9] Joskow, P. L. “Electricity Sector Restructuring and Competition.” Annual Review of Economics – https://www.annualreviews.org/doi/10.1146/annurev.economics.080109.130305
[10] Varian, H. R. “The Demand for Bandwidth.” Telecommunications Policy – https://www.sciencedirect.com/science/article/pii/S0308596101000361
[11] Courty, P. “Ticket Pricing under Demand Uncertainty.” Journal of Law and Economics – https://www.journals.uchicago.edu/doi/10.1086/340282
[12] Crew, M. A., & Kleindorfer, P. R. The Economics of Public Utility Regulation – https://mitpress.mit.edu/9780262031718/
