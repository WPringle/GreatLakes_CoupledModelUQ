import numpy as np
from wrf_fvcom.variables import PerturbedVariable, VariableDistribution
from surrogate.tree_regression import surrogate_model_predict

###########################################
#  ____     ___    ____     ___    _      #
# / ___|   / _ \  | __ )   / _ \  | |     #
# \___ \  | | | | |  _ \  | | | | | |     #
#  ___) | | |_| | | |_) | | |_| | | |___  #
# |____/   \___/  |____/   \___/  |_____| #
#                                         #
###########################################


class smethod(object):
    def __init__(self, variable_matrix, sens_names):
        self.dim = variable_matrix.shape[1]
        self.sens = dict((k, [None] * self.dim) for k in self.sens_names)
        self.sens_ready = dict((k, [False] * self.dim) for k in self.sens_names)
        self.ptypes = []
        for scheme in variable_matrix['scheme']:
            variable = PerturbedVariable.class_from_scheme_name(scheme)
            if variable.variable_distribution == VariableDistribution.DISCRETEUNIFORM:
                self.ptypes.append('int')
            else:
                self.ptypes.append('float')


class sobol(smethod):
    ## Main and total are based on Saltelli 2010; it computes joint in the total sense!
    ##
    ## Initialization
    def __init__(self, variable_matrix):
        print('Initializing SOBOL')
        self.sens_names = ['main', 'total', 'jointt']
        smethod.__init__(self, variable_matrix, self.sens_names)

    def sample(self, ninit, parameter_types=None):
        print('Sampling SOBOL')

        sam1 = np.random.rand(ninit, self.dim)
        sam2 = np.random.rand(ninit, self.dim)

        for pp, par_type in enumerate(self.ptypes):
            if par_type == 'int':
                sam1[:, pp] = np.round(sam1[:, pp])
                sam2[:, pp] = np.round(sam2[:, pp])

        xsam = np.vstack((sam1, sam2))

        for id in range(self.dim):
            samid = sam1.copy()
            samid[:, id] = sam2[:, id]
            xsam = np.vstack((xsam, samid))

        self.nsam = xsam.shape[0]
        self.sens_ready['main'] = True
        self.sens_ready['total'] = True
        self.sens_ready['jointt'] = True

        return xsam

    def compute(self, ysam, computepar=None):
        ninit = self.nsam // (self.dim + 2)
        y1 = ysam[ninit : 2 * ninit]
        var = np.var(ysam[: 2 * ninit])
        si = np.zeros((self.dim,))
        ti = np.zeros((self.dim,))
        jtij = np.zeros((self.dim, self.dim))

        for id in range(self.dim):
            y2 = ysam[2 * ninit + id * ninit : 2 * ninit + (id + 1) * ninit] - ysam[:ninit]
            si[id] = np.mean(y1 * y2) / var
            ti[id] = 0.5 * np.mean(y2 * y2) / var
            for jd in range(id):
                y3 = (
                    ysam[2 * ninit + id * ninit : 2 * ninit + (id + 1) * ninit]
                    - ysam[2 * ninit + jd * ninit : 2 * ninit + (jd + 1) * ninit]
                )
                jtij[id, jd] = ti[id] + ti[jd] - 0.5 * np.mean(y3 * y3) / var

        self.sens['main'] = si
        self.sens['total'] = ti
        self.sens['jointt'] = jtij.T

        return self.sens


def compute_sensitivities(surrogate_model, variable_matrix, sample_size=10000):

    # get the sensitivity sample matrix
    SensMethod = sobol(variable_matrix)
    xsam = SensMethod.sample(sample_size)
    # evaluate the surrogate model at the samples
    ysam = surrogate_model_predict(surrogate_model, xsam)

    npts = ysam.shape[1]
    variable_names = []
    variable_prior = ''
    for sdx, scheme in enumerate(variable_matrix['scheme']):
        variable_name = PerturbedVariable.class_from_scheme_name(scheme).name
        if variable_name != variable_prior:
            variable_names.append(variable_name)
        variable_prior = variable_name
    ndim = len(variable_names)
    sens_dict = {
        'main': np.zeros((npts, ndim)),
        'total': np.zeros((npts, ndim)),
        'variable_names': variable_names,
    }
    for i in range(npts):
        sens = SensMethod.compute(ysam[:, i])
        vdx = -1
        variable_prior = ''
        for sdx, scheme in enumerate(variable_matrix['scheme']):
            variable_name = PerturbedVariable.class_from_scheme_name(scheme).name
            if variable_name != variable_prior:
                vdx += 1
            variable_prior = variable_name
            sens_dict['main'][i, vdx] += sens['main'][sdx]
            sens_dict['total'][i, vdx] += sens['total'][sdx]

    return sens_dict
