# PhaseDiagram main file
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from matplotlib import colors
import warnings

# @param init_points: a numpy array of shape (N, 2). Initial set of points to define the grid.
# @param func:        the phase function. This should accept vectors in the same format as init_points
#                     and return a 1D vector of integers, of size (N,).
# @param num_refinements: The leve lof detail to go to.
# @param ax:         Plotting axes from matplotlib.
# ----------
# Returns: a Delaunay triangulation object, values for each point and and the boundary coordinates
def phase_optimise(init_points, func, num_refinements=4):
    vals = func(init_points)
    tri = Delaunay(init_points, incremental=True)
    boundary = []
    for n in range(num_refinements):
        print("Optimising: n=%d" % (n+1))
        vals, boundary = d_phase_optimise(tri, vals, func)
        if len(boundary) == 0:
            print('No phase boundaries found.')
            break
    
    return tri, vals, boundary
    


def d_phase_optimise(tri, vals, func):
    boundary = []
    for simplex in tri.simplices:
        x = vals[simplex]
        if not np.all(x == x[0]):
            boundary.append(np.mean(tri.points[simplex],axis=0))
#         if x[0] != x[1]:
#             boundary.append(0.5*(tri.points[simplex][0] + tri.points[simplex][1]))
#         if x[0] != x[2]:
#             boundary.append(0.5*(tri.points[simplex][0] + tri.points[simplex][2]))
#         if x[1] != x[2]:
#             boundary.append(0.5*(tri.points[simplex][1] + tri.points[simplex][2]))

    vals = np.append(vals, func(np.array(boundary)))

    tri.add_points(boundary)

    return vals, boundary
    


def genradgrid(n_radii, n_angles, max_radius=1, min_radius=None):
    if min_radius is None:
        min_radius = max_radius/100
        
    radii = np.linspace(min_radius, max_radius, n_radii)

    angles = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)
    angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)
    angles[:, 1::2] += np.pi / n_angles

    return np.vstack(((radii * np.cos(angles)).flatten(), (radii * np.sin(angles)).flatten())).T
    

# @param phase_func - accepts 1 vectorised inputs e.g. F([[x1,y1],[x2,y2],...]) and returns an integer between 0 and N-1, where N is the number of named phases
# @param phase_names - a list of length N for labelling the phases
# @param init_points - an initial list of [ [J1,J2], ... ] 
# @param num_refinements - number of subtriangulations to calculate
# @param cmap - matplotlib colormap
# @param show_boundary - one of:
#                        + dict of keyword arguments for the call to plt.plot() on how to style the phase boundary
#                        + True to show default style
#                        + None or False to hide phase boundary plotting
# @param show_triangulation - one of:
#                        + dict of keyword arguments for the call to plt.plot() on how to style the traingulation
#                        + True to show default style
#                        + None or False to hide traingulation
    
def plot_phasedia(phase_func, phase_names, init_points, num_refinements=6, cmap='Pastel2',
                  show_boundary=True, show_triangulation=None):
    t,v,b = phase_optimise(init_points, phase_func, num_refinements=num_refinements)
    d_plot_phasedia(t,v,b, phase_names, cmap, show_boundary, show_triangulation)



def d_plot_phasedia(tri, vals, boundary, phase_names, cmap='Pastel2',
                  show_boundary=True,
                  show_triangulation=None):
    # define boundaries for the colormap
    bounds = np.arange(len(phase_names)+1,dtype=np.float64)-0.5
    norm = colors.BoundaryNorm(bounds, len(bounds))

    fig, ax= plt.subplots()

    ax.axis('equal')
    c = ax.tripcolor(tri.points[:,0], tri.points[:,1], tri.simplices, vals, cmap=cmap, norm=norm)
    
    ##########################
    # Format the triangulation (good intellectual honesty to show this, it removes ambiguity as to which points were evaluated)
    if show_triangulation is not None:
        if type(show_triangulation) is not dict:
            ax.triplot(tri.points[:,0], tri.points[:,1], tri.simplices, color='w',lw=0.2)
        elif show_triangulation is not False:
            ax.triplot(tri.points[:,0], tri.points[:,1], tri.simplices, **show_triangulation)
    
#     #######################
    # format the colorbar
    cbar = fig.colorbar(c, location='right',aspect=14)
    cbar.ax.get_yaxis().set_ticks([])
    bounds = cbar.ax.get_ylim()
    x = 0.5*(cbar.ax.get_xlim()[0] + cbar.ax.get_xlim()[1])
    
    for j, name in enumerate(phase_names):
        cbar.ax.text(x, j , name, ha='center', va='center')

    # Plot the phase boundaries in another colour to hide the ugly interpolated colouring
    if show_boundary is not None:
        if len(boundary)==0:
            warnings.warn('There is no boundary to show!')
        elif type(show_boundary) is dict:
            X, Y = np.array(boundary).T
            ax.plot(X, Y, **show_boundary)
        elif show_boundary is not False:
            sb = {'color':'white', 'ms':3, 'marker': '.', 'linestyle':'None'}
            X, Y = np.array(boundary).T
            ax.plot(X, Y, **sb)
    
    return fig, ax
    
        

        
# cursed coordinate functions for 3D map projecitons

# azimuthal (polar) projection
# God's flat earth
def azim_XY_to_xyz(XY):
    lens = np.linalg.norm(XY,axis=1)
    return (np.sin(lens)*XY[:,0]/lens, np.sin(lens)*XY[:,1]/lens, np.cos(lens))

def azim_xyz_to_XY(x,y,z):
    n = (x**2 + y**2 + z**2)**-0.5
    
    rho = np.arccos(n*z)
    srho = np.sin(rho) + 1e-6
    return (n*x*rho/srho, n*y*rho/srho)


# mercator projection
def mercator_XY_to_xyz(XY):
    return (np.sin(-XY[:,1])*np.cos(XY[:,0]), np.sin(-XY[:,1])*np.sin(XY[:,0]), np.cos(-XY[:,1]))

def mercator_xyz_to_XY(x,y,z):
    n = (x**2 + y**2 + z**2)**-0.5
    phi = np.arctan2(y,x)
    theta = -np.arccos(n*z)
    if np.isscalar(phi):
        if np.isscalar(theta):
            return (phi, theta)
        else:
            return (phi*np.ones_like(theta), theta)
    elif np.isscalar(theta):
        return (phi, theta*np.ones_like(phi))
    else:
        return (phi, theta)
    
class PhasePlane:
    # @param phase_func accepting three vectors x,y,z and returning an integer
    #                   phase_func(x,y,z) ---> int
    #                   These integers are used to index phase names
    # @param phase_names, a list of strings e,g, ['ferromagnet', 'antiferromagnet']
    # @param projection: either "azimuthal" or "mercator"
    def __init__(self, phase_func, phase_names, param_names):
        self.func = phase_func
        self.phase_names = phase_names
        self.param_names = param_names
        self.initpts = None
        self.tri=None
        self.vals=None
        self.boundary=None
        self.num_refinements = 0
        
    # If Y is provided, defines the initial grid bsed on the Cartesian product X, Y
    # Otherwise, directly uses X as a list of points 
    def set_initpts(self, X, Y=None):
        if Y is None:
            # assume X is a list of points
            assert len(np.asarray(X).shape) ==2
            self.initpts = X
        else:
            # assume it's a grid
            self.initpts= np.vstack((np.repeat(X, len(Y)), np.tile(Y, len(X)))).T
        
    # Calculates n triangular refinements of the grid.
    def refine(self, n=1):
        def pfunc(XY):
            return self.func(*(XY.T))
            
        if self.tri is None:
            if self.initpts is None:
                raise Exception("No initialisation points provided. Use PhasePlane.set_initpts() first")
            # No triangulation, need to calculate it from initpts
            self.tri, self.vals, self.boundary = phase_optimise(self.initpts, pfunc, num_refinements=n)
            self.num_refinements = n
        else:
            #refine an existing triangulation
            for i in range(n):
                self.vals, self.boundary = d_phase_optimise(self.tri, self.vals, pfunc)
            self.num_refinements += n
            
    # Use this to plot the phase diagram.
    # @param cmap - what it says on the tin. Works best when it is a qualitative colormap.
    # @param show_boundary - one of:
    #                        + dict of keyword arguments for the call to plt.plot() on how to style the phase boundary
    #                        + True to show default style
    #                        + None or False to hide phase boundary plotting
    # @param show_triangulation - one of:
    #                        + dict of keyword arguments for the call to plt.plot() on how to style the traingulation
    #                        + True to show default style
    #                        + None or False to hide traingulation
    def plot(self, cmap='Pastel2', show_boundary=True, show_triangulation=None):
        if self.tri is None:
            self.tri, self.vals, self.boundary = phase_optimise(self.initpts, pfunc, num_refinements=0)
            
        self.fig, self.ax = d_plot_phasedia(self.tri, self.vals, self.boundary, self.phase_names,
                                            cmap, show_boundary, show_triangulation)
        
        self.ax.set_xlabel(self.param_names[0])
        self.ax.set_ylabel(self.param_names[1])
    
    
    
# Plots a phase diagram over a 2D projection of the unit sphere.
class PhaseSphere:
    # @param phase_func accepting three vectors x,y,z and returning an integer
    #                   phase_func(x,y,z) ---> int
    #                   These integers are used to index phase names
    # @param phase_names, a list of strings e,g, ['ferromagnet', 'antiferromagnet']
    # @param projection: either "azimuthal" or "mercator"
    def __init__(self, phase_func, phase_names, param_names, projection = 'azimuthal'):
        self.func = phase_func
        self.phase_names = phase_names
        self.param_names = param_names
        self.set_projection(projection)
        self.tri=None
        self.vals=None
        self.boundary=None
        self.num_refinements = 0
        
        
    # @param num_theta, num_phi: dimensions of the grid on which to evaluate the initial (coarse) grid
    def set_projection(self,projection=None, num_theta = 5, num_phi=20):
        if projection is None:
            projection = self.projection
        else:
            self.projection = projection
        
        if projection == "azimuthal":
            self.figsize = (7.5,6)
            self.initpts = genradgrid(num_theta, num_phi, max_radius=np.pi)
            self.XY_to_xyz = azim_XY_to_xyz
            self.xyz_to_XY = azim_xyz_to_XY

            # No cuts necessary
            self.const_parameterisations = [np.append(np.linspace(0,2*np.pi,250),0)]


        elif projection == "mercator":
            self.figsize=(13.5,6)
            
            phi = np.linspace(-np.pi,np.pi,num_phi)
            theta = np.linspace(0, -np.pi, num_theta)

            self.initpts= np.vstack((np.repeat(phi, num_theta), np.tile(theta, num_phi))).T

            self.XY_to_xyz = mercator_XY_to_xyz
            self.xyz_to_XY = mercator_xyz_to_XY
            
            self.const_parameterisations = [np.linspace(j*np.pi/2+1e-2,(j+1)*np.pi/2-1e-2,50) for j in range(4)]

        elif projection == "elliptical":
            raise NotImplementedException()
        else:
            print(projection)
            raise RuntimeError("No such projection is supported, try 'azimuthal', 'elliptical' or 'mercator'")
            
    # defines the initial grid
    def set_initpts(self, ntheta, nphi):
        self.set_projection(num_theta=ntheta, num_phi=nphi)
        
    # Calculates n triangular refinements of the grid.
    def refine(self, n=1):
        def pfunc(XY):
            return self.func(*self.XY_to_xyz(XY))
            
        if self.tri is None:
            # No triangulation, need to calculate it from initpts
            self.tri, self.vals, self.boundary = phase_optimise(self.initpts, pfunc, num_refinements=n)
            self.num_refinements = n
        else:
            #refine an existing triangulation
            for i in range(n):
                self.vals, self.boundary = d_phase_optimise(self.tri, self.vals, pfunc)
            self.num_refinements += n
        
    # Plots a contour of constant [param] = [val]. 
    # If the total extent of the contour is too small, a single oversized dot is plotted in the same colour.
    def plot_contour(self, param, val, color, linewidth = 0.3):
        if np.abs(val)>1:
            raise Exception("val must lie on the unit sphere")
            
        rho = np.sqrt(1-val**2)
        for t in self.const_parameterisations:
            V = [0,0,0]
            V[param] = val
            V[(param+1)%3] = rho*np.cos(t)
            V[(param+2)%3] = rho*np.sin(t)

                
            
            X,Y = self.xyz_to_XY(V[0], V[1], V[2])
            if np.var(X) + np.var(Y)>1e-2:
                self.ax.plot(X, Y, lw=linewidth, color=color)
            else:
                self.ax.scatter(np.mean(X), np.mean(Y), color=color)
        
    # Use this to plot the phase diagram.
    # @param cmap - what it says on the tin. Works best when it is a qualitative colormap.
    # @param show_boundary - one of:
    #                        + dict of keyword arguments for the call to plt.plot() on how to style the phase boundary
    #                        + True to show default style
    #                        + None or False to hide phase boundary plotting
    # @param show_triangulation - one of:
    #                        + dict of keyword arguments for the call to plt.plot() on how to style the traingulation
    #                        + True to show default style
    #                        + None or False to hide traingulation
    # @param contours - the lines of constant Xparam, Yparam, Zparam to show
    
    def plot(self, cmap='Pastel2', show_boundary=True, show_triangulation=None, contours = [-1+1e-6, -0.5,0,0.5,1-1e-6]):
        if self.tri is None:
            self.tri, self.vals, self.boundary = phase_optimise(self.initpts, pfunc, num_refinements=0)
            
        self.fig, self.ax = d_plot_phasedia(self.tri, self.vals, self.boundary, self.phase_names,
                                            cmap, show_boundary, show_triangulation)
        self.fig.set_size_inches(*self.figsize)

        ax = self.ax
        
        # Plot lines of constant parameters
        for d in contours:
            rho = np.sqrt(1-d**2)
            sr2 = np.sqrt(2)
            
            ax.text(*self.xyz_to_XY(d, -rho/sr2,-rho/sr2), "%s=%.1f" % (self.param_names[0], d), color='red') 
            self.plot_contour(0, d, 'red')
            
            ax.text(*self.xyz_to_XY(rho/sr2,d,rho/sr2), "%s=%.1f" % (self.param_names[1], d), color='green') 
            self.plot_contour(1, d, 'green')
            
            if self.projection == "mercator":
                ax.text(*self.xyz_to_XY(-rho,0,d), "%s=%.1f" % (self.param_names[2], d), color='blue') 
            else:
                ax.text(*self.xyz_to_XY(-rho/sr2,rho/sr2,d), "%s=%.1f" % (self.param_names[2], d), color='blue') 
            self.plot_contour(2, d, 'blue')

        self.ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False) 
        self.ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False) 

    # plots a point on the phase diagram corresponding to x,y,z
    # note that these are projected to the unit sphere
    def add_point(self, x,y,z,**kwargs):
        N = (x**2 + y**2 + z**2)**(-0.5)
        x *= N
        y *= N
        z *= N
        self.ax.plot(*self.xyz_to_XY(x,y,z),**kwargs)
        
    # plots a labeled point on the phase diagram corresponding to x,y,z
    # note that these are projected to the unit sphere
    def add_text(self, x,y,z, label, text_kwargs={}, **kwargs):
        N = (x**2 + y**2 + z**2)**(-0.5)
        x *= N
        y *= N
        z *= N
        self.ax.text(*self.xyz_to_XY(x,y,z),label,**kwargs)
        
    

    
