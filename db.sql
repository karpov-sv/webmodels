DROP TABLE IF EXISTS models CASCADE;
CREATE TABLE models (
       id SERIAL PRIMARY KEY,
       name  TEXT UNIQUE,

       meta TEXT,

       Lstar FLOAT,
       Mdot FLOAT,
       Tstar FLOAT,
       Teff FLOAT,
       vel_law INT,
       cl_par_1 FLOAT,
       cl_par_2 FLOAT,

       hyd_mass_frac FLOAT,
       hyd_rel_frac FLOAT,

       ions TEXT[],
       params hstore,
       vadat hstore,

       maxcorr FLOAT
);

DROP TABLE IF EXISTS species CASCADE;
CREATE TABLE species (
       id SERIAL PRIMARY KEY,
       model INT REFERENCES models (id) ON DELETE CASCADE,
       name TEXT,
       mass_frac FLOAT,
       rel_frac FLOAT,
       z_z_sun FLOAT,
       z_sun FLOAT
);
CREATE INDEX ON species (model);
CREATE INDEX ON species (name);

DROP TABLE IF EXISTS obs_fin CASCADE;
CREATE TABLE obs_fin (
       id SERIAL PRIMARY KEY,
       model INT REFERENCES models (id) ON DELETE CASCADE,
       freq FLOAT,
       lambda FLOAT,
       fnu FLOAT,
       flambda FLOAT
);
CREATE INDEX ON obs_fin (model);
CREATE INDEX ON obs_fin (freq);
CREATE INDEX ON obs_fin (lambda);

DROP TABLE IF EXISTS obs_cont CASCADE;
CREATE TABLE obs_cont (
       id SERIAL PRIMARY KEY,
       model INT REFERENCES models (id) ON DELETE CASCADE,
       freq FLOAT,
       lambda FLOAT,
       fnu FLOAT,
       flambda FLOAT
);
CREATE INDEX ON obs_cont (model);
CREATE INDEX ON obs_cont (freq);
CREATE INDEX ON obs_cont (lambda);
