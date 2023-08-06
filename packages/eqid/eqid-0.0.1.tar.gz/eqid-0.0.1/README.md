# eqid

Python package to retrieve the most recent earthquake information in Indonesia.

# How does it work?

This package collect data from BMKG, the official government-run agency for meteorology, climatology, and geophysics.

# How to use

Call the function

```
import eqid

result = eqid.get_data()
```

The variable result will contain a dictionary with the detail of the latest earthquake.

```
{'date': '15 September 2021', 
 'time': '07:49:47 WIB', 
 'magnitude': 5.4, 
 'depth': 20,
 'location': {'lat': 1.28, 'long': 122.16}, 
 'center_description': 'Pusat gempa berada di laut 85 km BaratLaut Boalemo',
 'affected_description': 'Dirasakan (Skala MMI): III Boalemo, II - III Buol, 
 II Manado, II Bone Bolango, II Gorontalo, II Toli-toli'}
```