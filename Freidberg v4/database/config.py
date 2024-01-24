root_tag = 'dataSchema'

cat1 = 'reactor/geometry'
cat2 = 'reactor/plasma'
cat3 = 'reactor/blanket'
cat4 = 'reactor/coils'
cat5 = 'reactor/other'
cat6 = 'reference'
cat7 = 'scaledData'
x_root = '/' + root_tag

x_R0 = '/'.join([x_root, cat1, 'R0'])
x_a = '/'.join([x_root, cat1, 'a'])
x_b = '/'.join([x_root, cat1, 'b'])
x_c = '/'.join([x_root, cat1, 'c'])

x_T = '/'.join([x_root, cat2, 'T'])
x_n = '/'.join([x_root, cat2, 'n'])
x_En = '/'.join([x_root, cat2, 'En'])
x_Ealpha = '/'.join([x_root, cat2, 'Ealpha'])
x_ELi = '/'.join([x_root, cat2, 'ELi'])
x_etat = '/'.join([x_root, cat2, 'etat'])
x_PW = '/'.join([x_root, cat2, 'PW'])

x_lambdabr = '/'.join([x_root, cat3, 'lambdabr'])
x_lambdasd = '/'.join([x_root, cat3, 'lambdasd'])
x_Et = '/'.join([x_root, cat3, 'Et'])
x_gammafrac = '/'.join([x_root, cat3, 'gammafrac'])

x_sigma = '/'.join([x_root, cat4, 'sigma'])
x_Bc = '/'.join([x_root, cat4, 'Bc'])
x_Pcoil = '/'.join([x_root, cat4, 'Pcoil'])

x_PE = '/'.join([x_root, cat5, 'PE'])
x_VIPE = '/'.join([x_root, cat5, 'VIPE'])

x_sigmav = '/'.join([x_root, cat6, 'sigmav'])
x_mu0 = '/'.join([x_root, cat6, 'mu0'])

