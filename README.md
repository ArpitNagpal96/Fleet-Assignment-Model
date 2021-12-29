# Westjet-Fleet-Optimization
WestJet is a Canadian airline company that began its operations in 1996 as a low-cost carrier. As is the case for most airlines, WestJet also faces the challenging task of meeting the resurging demand while maintaining efficient scheduling of flights.
The project aims to find the optimal fleet assignment for WestJet to maximize its profits while accommodating different demand markets. Aircraft fuel, salaries, airport fees, and maintenance account for 66% of operating expenses (Appendix Figure 1), which are highly dependent on the fleet assignment of specific aircraft types to the appropriate routes according to a given schedule. Moreover, fleet assignment influences the number of spilled passengers and the loss of potential
revenue. While having different fleet types allows airlines to accommodate flight legs over different distances, costs, and demands, a suboptimal assignment may overturn the benefits of such flexibility.
The fleet assignment problem is a key component of the schedule planning process. The assignment task is performed after determining a preliminary flight schedule. 

The optimization model aims at maximizing the profit margin for WestJet based on the proposed fleet assignment.

The dataset utilized for this model is publicly available on OpenFlights. The available spreadsheet contained information on each of the 305 flight routes that WestJet operates across North America (US and Canada). Namely, it allowed us to know the following for each origin-destination pair: flight number, distance, duration, origin, destination, departure time, stipulated arrival time. For estimation of operational costs, route fares and demand, we analyzed WestJet’s
financial reports and extrapolated aggregate values for the same for all 305 routes.
