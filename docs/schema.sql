CREATE TABLE waste_categories (
    category_id SERIAL PRIMARY KEY,
    waste_type VARCHAR(100) NOT NULL UNIQUE,
    energy_saved_kwh_per_tonne NUMERIC(10, 2) NOT NULL,
    crude_oil_saved_barrels_per_tonne NUMERIC(10, 2)
);

CREATE TABLE annual_waste_records (
    record_id SERIAL PRIMARY KEY,
    year INT NOT NULL,
    category_id INT REFERENCES waste_categories(category_id),
    total_waste_generated_tonnes NUMERIC(12, 2) NOT NULL,
    total_waste_recycled_tonnes NUMERIC(12, 2) NOT NULL,
    recycling_rate_pct NUMERIC(5, 2),
    total_energy_saved_gwh NUMERIC(12, 4)
);

CREATE TABLE smart_bins (
    bin_id SERIAL PRIMARY KEY,
    location_name VARCHAR(150) NOT NULL,
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    category_id INT REFERENCES waste_categories(category_id),
    capacity_kg NUMERIC(8, 2) NOT NULL,
    status VARCHAR(30) DEFAULT 'active'
);

CREATE TABLE bin_telemetry_logs (
    log_id SERIAL PRIMARY KEY,
    bin_id INT REFERENCES smart_bins(bin_id),
    fill_level_pct NUMERIC(5, 2) NOT NULL,
    weight_kg NUMERIC(8, 2),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
