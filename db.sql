DROP TABLE IF EXISTS models CASCADE;
CREATE TABLE models (
       id SERIAL PRIMARY KEY,
       name  TEXT UNIQUE,

       meta TEXT,

       Lstar FLOAT,
       Mdot FLOAT,
       Tstar FLOAT,
       Teff FLOAT,
       logg FLOAT,
       vel_law INT,
       Vinf FLOAT,

       cl_par_1 FLOAT,
       cl_par_2 FLOAT,

       hyd_mass_frac FLOAT,
       hyd_rel_frac FLOAT,

       carb_rel_frac FLOAT,
       nit_rel_frac FLOAT,
       oxy_rel_frac FLOAT,
       iron_rel_frac FLOAT,

       ions TEXT[],
       params hstore,
       vadat hstore,

       type TEXT,

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

DROP TABLE IF EXISTS spectra CASCADE;
CREATE TABLE spectra (
       id SERIAL PRIMARY KEY,
       model INT REFERENCES models (id) ON DELETE CASCADE,
       lambda FLOAT,
       flux FLOAT,
       cont FLOAT,
       fluxnorm FLOAT
);
CREATE INDEX ON spectra (model);
CREATE INDEX ON spectra (lambda);
