node 'mo3' {                                               
        class { 'epel':}                                   
        class { 'imars-processing': }                      

        include cpan

}

#node 'seashell.marine.usf.edu' {
#       class {'imars':}         
#}                               

node 'seastar.marine.usf.edu' {
        class { 'epel':}       
        class {'pyhdf':}       
        package{'python-matplotlib':
                ensure => 'present',
        }                           
        package{'gdal':             
                ensure => 'present',
        }                           
        package{'gdal-devel':       
                ensure => 'present',
        }                           
        package{'gdal-python':      
                ensure => 'present',
        }                           
        python::pip { 'pypng':      
                pkgname => 'pypng', 
        }                           
        package{'h5py':             
                ensure => 'present',
        }                           
}                                   

node 'carbon.marine.usf.edu' {
        class { 'epel':}      
        class {'pyhdf':}      
        package{'python-matplotlib':
                ensure => 'present',
        }                           
        package{'gdal':             
                ensure => 'present',
        }                           
        package{'gdal-devel':       
                ensure => 'present',
        }                           
        package{'gdal-python':      
                ensure => 'present',
        }                           
        python::pip { 'pypng':      
                pkgname => 'pypng', 
        }                           
        package{'h5py':             
                ensure => 'present',
        }                           
        package{'hdf5':             
                ensure => 'present',
        }                           
}                                   

node 'yin.marine.usf.edu' {
  class { 'nfs::server':   
    nfs_v4 => true,        
    nfs_v4_idmap_domain => 'yinmaster',
    nfs_v4_export_root => '/yin',      
    nfs_v4_export_root_clients =>      
      '192.168.1.0/24(rw,insecure,sync,no_subtree_check,insecure_locks,no_root_squash)'

  }
  nfs::server::export{ '/homes':
    ensure  => 'mounted',       
    tag => 'homes',             
    clients => '131.247.136.0/22(rw,insecure,sync,no_subtree_check,insecure_locks,no_root_squash)'
  }
}

  # By default, mounts are mounted in the same folder on the clients as
  # they were exported from on the server

node 'seashell.marine.usf.edu' {
  class { 'nfs::server':
    nfs_v4 => true,
#    nfs_v4_export_root_clients =>
#      '/yin 131.247.136.0/22(rw,fsid=root,insecure,no_subtree_check,async,no_root_squash)'
  }
  Nfs::Client::Mount <<| |>> {
    ensure => 'mounted',
    mount  => '/home1',
  }
}
