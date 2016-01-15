#!/usr/bin/env python

import numpy as np
import posixpath, glob, datetime, os, sys, re, StringIO
import psycopg2, psycopg2.extras

def my_float(string):
    string = string.replace('D', 'E')

    try:
        return float(string)
    except:
        idx = string.find('-')
        if idx < 0:
            print "Can't parse float:" + string
            return string
        else:
            s = string.split('-')

            return float(s[0]+'E-'+s[1])

def read_obs(filename):
    with open(filename) as ff:
        lines = ff.readlines()
        state = 0
        freq,intens = [],[]

        for line in lines:
            s = line.split()
            if not s:
                state += 1
            else:
                if state == 3:
                    for ss in s:
                        freq.append(my_float(ss))

                elif state == 6:
                    for ss in s:
                        intens.append(my_float(ss))

        freq,fnu = [np.array(_) for _ in freq,intens]
        freq *= 1e15
        fnu *= 1e-23
        l = 1e8*29979245800/freq
        flambda = fnu*freq/l #  29979245800/(l*1e-8)**2/1e8

        l1 = np.array(range(900,10000,1) + range(10000, 40000, 10))
        freq1 = np.interp(l1, l, freq)
        intens1 = np.interp(l1, l, intens)
        fnu1 = np.interp(l1, l, fnu)
        flambda1 = np.interp(l1, l, flambda)

        return {'freq':freq1, 'fnu':intens1, 'lambda':l1, 'flambda':flambda1}

def read_model(dir):
    model = {'params':{}, 'ions':[], 'species':{}, 'vadat':{}}
    model['dir'] = dir
    model['name'] = posixpath.split(dir)[-1]

    if not posixpath.exists(posixpath.join(dir, 'MOD_SUM')) or not posixpath.exists(posixpath.join(dir, 'VADAT')) or not posixpath.exists(posixpath.join(dir, 'obs', 'obs_fin')) or not posixpath.exists(posixpath.join(dir, 'obs', 'obs_cont')):
        return None

    with open(posixpath.join(dir, 'VADAT')) as ff:
        lines = ff.readlines()

        for line in lines:
            if line[0] == '!':
                continue
            m = re.match('^\s*(\S+)\s+\[(\S*)\]', line)
            if m:
                model['vadat'][m.group(2)] = m.group(1)

        if model['vadat']['CL_LAW'] != 'EXPO':
            print "Incorrect CL_LAW = %s" % model['vadat']['CL_LAW']
            return None

    with open(posixpath.join(dir, 'MOD_SUM')) as ff:
        lines = ff.readlines()
        state = 0
        just_skipped = False

        for line in lines:
            s = line.split()
            if not s:
                if not just_skipped:
                    state += 1
                just_skipped = True
            else:
                just_skipped = False

                if state == 1:
                    model['time'] = model.get('time','') + line

                elif state == 2:
                    for ss in s:
                        model[ss.split('[')[0]] = int(ss.split('[')[1][:-1])

                elif state == 3:
                    for ss in s:
                        model['ions'].append(ss.split('[')[0])

                elif state == 4 or state == 5:
                    line = line.replace('R ', 'R*')
                    line = line.replace('Log g', 'Log_g')
                    s = line.split()
                    for ss in s:
                        sss = ss.split('=')
                        model['params'][sss[0]] = my_float(sss[1])

                elif state == 7:
                    if s[0] != 'SPECIES':
                        model['species'][s[0]] = {'rel_frac':my_float(s[1]), 'mass_frac':my_float(s[2]), 'z_z_sun':my_float(s[3]), 'z_sun':my_float(s[4])}

                elif state == 9 or (state == 8 and model['vadat']['DO_CL'] == 'F'):
                    model['maxcorr'] = my_float(line.split(':')[1])

    model['obs_fin'] = read_obs(posixpath.join(dir, 'obs', 'obs_fin'))
    model['obs_cont'] = read_obs(posixpath.join(dir, 'obs', 'obs_cont'))

    return model

def query(conn, string="", data=(), simplify=True, debug=False):
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    if debug:
        print cur.mogrify(string, data)

    if data:
        cur.execute(string, data)
    else:
        cur.execute(string)

    try:
        result = cur.fetchall()
        # Simplify the result if it is simple
        if simplify and len(result) == 1:
            if len(result[0]) == 1:
                return result[0][0]
            else:
                return result[0]
        else:
            return result
    except:
        # Nothing returned from the query
        return None

if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option('-d', '--dbname', help='database name, defaults to webmodels', action='store', dest='dbname', default='webmodels')
    parser.add_option('-r', '--reprocess', help='Re-upload models already in database', action='store_true', dest='reprocess', default=False)
    parser.add_option('-t', '--type', help='Star type, default to WR', action='store', dest='type', default='WR')

    (options, args) = parser.parse_args()

    conn = psycopg2.connect("dbname=%s" % options.dbname)
    conn.autocommit = True
    #conn.set_session(readonly=readonly)
    psycopg2.extras.register_hstore(conn)

    for dir in args:
        model = read_model(dir)

        if not model:
            print "Wrong model in dir %s" % dir
            continue

        print model['dir'], model['params']['L*'], model['params']['Mdot'], model['params']['T*'], model['params']['Teff'], model['vadat']['VEL_LAW'], model['vadat']['CL_PAR_1'], model['vadat']['CL_PAR_2'], model['species']['HYD']['mass_frac'], model['species']['HYD']['rel_frac']

        if model['maxcorr'] > 1e3:
            print "maxcorr=%g is too large" % model['maxcorr']
            continue

        if not options.reprocess and query(conn, 'SELECT true FROM models WHERE name=%s', (model['name'],)):
            print "Model already in database, skipping"
            continue

        params={k:str(model['params'][k]) for k in model['params'].keys()}

        query(conn, "DELETE FROM models WHERE name=%s", (model['name'],))
        id = query(conn, "INSERT INTO models (name,meta,ions,params,vadat,Lstar,Mdot,Tstar,Teff,vel_law,Vinf,cl_par_1,cl_par_2,hyd_mass_frac,hyd_rel_frac,type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id", (model['name'], model['time'], model['ions'], params,model['vadat'], model['params']['L*'], model['params']['Mdot'], model['params']['T*'], model['params']['Teff'], int(model['vadat']['VEL_LAW']), model['params']['Vinf1'], float(model['vadat']['CL_PAR_1']), float(model['vadat']['CL_PAR_2']), model['species']['HYD']['mass_frac'], model['species']['HYD']['rel_frac'], options.type))

        query(conn, 'UPDATE models SET carb_rel_frac=%s, nit_rel_frac=%s, oxy_rel_frac=%s, iron_rel_frac=%s WHERE id=%s', (model['species']['CARB']['rel_frac'], model['species']['NIT']['rel_frac'], model['species']['OXY']['rel_frac'], model['species']['IRON']['rel_frac'], id))

        if model['params'].has_key('Log_g'):
            query(conn, 'UPDATE models SET logg=%s WHERE id=%s', (model['params']['Log_g'], id))

        for s in model['species'].keys():
            query(conn, "INSERT INTO species (model,name,mass_frac,rel_frac,z_z_sun,z_sun) VALUES (%s,%s,%s,%s,%s,%s)", (id, s, model['species'][s]['mass_frac'], model['species'][s]['rel_frac'], model['species'][s]['z_z_sun'], model['species'][s]['z_sun']))

        s = StringIO.StringIO()
        s.writelines(["%d\t%g\t%g\t%g\t%g\n" % (id, model['obs_fin']['lambda'][i], model['obs_fin']['flambda'][i], model['obs_cont']['flambda'][i], model['obs_fin']['flambda'][i]/model['obs_cont']['flambda'][i]) for i in xrange(len(model['obs_fin']['lambda']))])
        s.seek(0)
        cur = conn.cursor()
        cur.copy_from(s, 'spectra', columns=('model','lambda','flux','cont','fluxnorm'))
        conn.commit()

        print "uploaded"
