
To install, run the following command -

```source install.sh```

This performs the following steps - 

1. Creates a conda environment ('ferment')
2. Installs dependencies to the created environment 
3. Creates and populates a database ('ferment.db')

To activate the new environment, run the following command -

```conda activate ferment```

The created database represents spectrum data for the production of pigments by growing microorganisms in fermentors.

To understand the database better, see the below diagram representing the relationships between each table. 

![](ferment.jpg)


Notes

1. I used an ORM approach with sqlalchemy 
2. Although these things do very much matter, I haven't considered the following -
   - Data validation
   - Speed/Memory optimization
   - Error handling
   - Testing
3. I was not able to complete the calculation task unfortunately (I kept running into issues with google drive). 
   So long as you have the sample and blank data .csv files loaded as pandas DataFrames, you can create a table of 
   'calibrated' data with the below code snippet, from which, you can select out the values at '534.0', average 
   them (or sum; it wasn't entirely clear), and plug them into the formula.

```
    calibrated_df = sample_df.copy()
    calibrated_df.iloc[:, 2:] = sample_df.iloc[:, 2:].sub(blank_df.iloc[:, 2:])
    
    absorbance = calibrated_df['534.0'].mean()
    concentration = absorbance * 0.033 * 1
```

4. To be consistent with how my code behaves, I have denoted a one-to-one relationship between a fermentation process 
   and a sample. However, I can see why this might be wrong in practice.
5. Location could be its own table 
