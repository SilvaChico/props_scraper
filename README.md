# Property scraping

- [ ] Create data model

  - Property
    - title
    - price
    - location (table)
    - description
    - image (maybe ?)
    - url
    - date
    - source (table)
    - type
    - area
    - contact (table)

  - Location
    - city
    - district
    - street
    - number
    - floor
    - coordinates / google place id

  - Source
    - name
    - url
    - branch
    - type
    - contact (table)

  - Contact (sales person)
    - name
    - phone
    - email
    - url
    - source (table)

- [ ] Scrape data every 15 minutes
  - [ ] Get data from source
  - [ ] Save data to database
  - [ ] Add button to scrape data manually
