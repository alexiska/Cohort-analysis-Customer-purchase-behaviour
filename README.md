# Cohort-analysis-Customer-purchase-behaviour

 A time based cohort analysis has been performed to see the customers purchase activity. Customers are grouped into cohort, based on their month of their first purchase and then calculte the number of month since the first purchase. Retention are then calculated and plotted on a heatmap.

## Attribute Information

* InvoiceNo: Invoice number. Nominal, a 6-digit integral number uniquely assigned to each transaction. If this code starts with letter 'c', it indicates a cancellation.
* StockCode: Product (item) code. Nominal, a 5-digit integral number uniquely assigned to each distinct product.
* Description: Product (item) name. Nominal.
* Quantity: The quantities of each product (item) per transaction. Numeric.
* InvoiceDate: Invice Date and time. Numeric, the day and time when each transaction was generated.
* UnitPrice: Unit price. Numeric, Product price per unit in sterling.
* CustomerID: Customer number. Nominal, a 5-digit integral number uniquely assigned to each customer.
* Country: Country name. Nominal, the name of the country where each customer resides. 

(Source: https://archive.ics.uci.edu/ml/datasets/Online+Retail)

### Python package used
* Pandas 
* Numpy 
* Matplotlib 
* Seaborn 
* Datetime

### Table Content 
* Exporatory data analysis (EDA)
* Data cleaning and manipulation
* Cohort analysis
* Conslusion

![](Images/Cohort.png)
