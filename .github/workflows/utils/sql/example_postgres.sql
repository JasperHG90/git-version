-- Create some table
CREATE TABLE IF NOT EXISTS public.test_table (
    id SERIAL PRIMARY KEY,
    age INT,
    category VARCHAR(10)
);

-- Drop the table
DROP TABLE IF EXISTS public.test_table;
