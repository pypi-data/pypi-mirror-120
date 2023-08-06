# AIOps4B

AIOps4B (AIOps for business) is a framework for business decision making. 

Below is the description of what the framework does...

**Trend Analysis, Root-cause identification and Predicting the future trends accordingly:**
AIOps4B performs trend analysis on a given time-series dataset (For e.g, Revenue values by date) with additional related metrics that has impact on the data (For e.g, product ratings, delivery timelines, discounts) to detect past trends with changepoints considering external events (for e.g. weather, seasonality, holidays), internal events (for e.g. marketing campaign). 

Each trend change point (for e.g. from down trend to up trend) will be labeled with its root-cause (for e.g. internal or external event, or some metrics that has impact on the Revenue) The un-known anomolies/events (for e.g. black friday) will need to be detected through manual analysis and then defined as internal/external events to be labeled. Once all past trends are identified/labeled with its root-cause, the future trends can be predicted after providing the related future events.

**Detailed Root-cause analysis & Recommendations:**

For each root-cause identified/labeled, it further defines the impact of each event and metrics to the overall trend as percentages (For e.g. the imapct of bad product rating is %25 on the Revenue, etc.) to make recommendations accordingly.

** Optimized Recommendations:**

After recommending that (for e.g. if the future Revenue is down), the reason of the past/future trends was because of an event or metric (for e.g. product reviews), it further make optimized recommendation after finding the real cause the problem (why the product reviews was bad and what to do with it)


**How it can be used:**

AIOps4B is designed as pyhton package currently with three API's. The pyhton package can be downloaded from 
https://pypi.org/project/aiops4b-NTTDataUK/

The package can be wrapped/deployed as REST API and embedded in any application / visualization dashboard in the future. As of now, it is used within a pyhton based dash application to display the results in interactive graphics.

- **Prediction API **predicts the future trends only and compares the predicted value with actuals on an interactive graph. It returns the graph representation, forecasted trend as a result. The graph can be displayed either on a Dash App or can be embedded into Visualization tools.

- **Recommendation API** analyzes the past trends and predicts the future trends with its root-causes and labels them on an interactive graph. It returns the graph representation and related recommendations (as what to do with each trend) as a result . The graph can be displayed either on a Dash App or can be embedded into Visualization tools.

- **Optimization API** analyzes the past trends and predicts the future trends with its root-causes and labels them on an interactive graph. It returns the graph representation and related recommendations (as what to do with each trend) as a result . The graph can be displayed either on a Dash App or can be embedded into Visualization tools.

**What are the use-cases it can be used in:**
- **Enrich existing KPI dashboards: **If the dataset is ready for a given KPI with its related metrics that is contributing to the revenue, the REST API's can be called to provide past/future complex trend analysis with each root causes and recommendations to fix the issues.
- Enrich applications with interactive trend analysis/recommendations - it can be embedded into applications of any sort.
- Respond to business queries: Integrate with Chatbots, Alexa, etc for business users to ask business questions about KPI's and metrics and get root-causes, recommendations to fix. This can an innovative enabler especially for executive stakeholders to respond to their queries such as "Can we achieve our Revenue targets in the coming quarter"?
- **End to end Business process analysis/issue mining:** It can be integrated with business processes (such as Order to Cash business process) to analyze the overall health of the Revenue generated and define the root causes and alert if the objective Revenue KPI is not met or will not be met in the coming days/months.

**Next steps:**
- Use it in real life projects and improve the existing functionality further.
- Extend the framework with self-learning. After making recommendations, it will need to analyze the outcomes and optimize itself.

