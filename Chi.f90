 Complex(kind = 8) function f(gamman, epsilon2, xq)
    implicit none

    complex(kind = 8), intent(in) :: gamman
    real(kind = 8), intent(in) :: epsilon2, xq

    real(kind = 8) :: energyUpper, energyLower, denergy
    integer, parameter :: dp = 8
    integer :: ienergy, Nenergy
    real(kind = 8) :: epsilon1
    real(kind = 8), parameter :: pi = acos(-1.0_dp)
    complex(kind = 8) :: csum

    Nenergy = 1000
    energyUpper = 20.0_dp
    energyLower = -energyUpper
    denergy = (energyUpper - energyLower)/dble(Nenergy)
    csum = dcmplx(0, 0)

    do ienergy = 1, Nenergy
    	epsilon1 = energyLower + (ienergy - 0.5_dp)*denergy
	csum = csum + denergy*1.0_dp/(sqrt(pi*(1.d0 - xq**2)))*1.0_dp/(gamman - epsilon1)*exp(-(epsilon1 - xq*epsilon2)**2/(1.d0 - xq**2))
    enddo

    f = csum

 end function f

 program main
 implicit none
 	integer :: narg
	character *100 :: buffer
	character *20 :: sigma_file
	character *20 :: mu_file
	integer, parameter :: dp = 8	
	integer :: Niom, Niom2
	Integer :: NiomMin = 100
	real(kind = 8) :: beta
	integer :: Niom_factor = 5
	integer :: Niom2_factor = 2
	real(kind = 8), dimension(:), allocatable :: xiom
	real(kind = 8), dimension(:), allocatable :: xiom2
	complex(kind = 8) :: ii = dcmplx(0, 1)
    	complex(kind = 8), dimension(:, :, :), allocatable :: sigma
	complex(kind = 8), dimension(:, :, :), allocatable :: sigma_temp
	integer :: norb = 2
	integer :: row, col
	integer :: nxq = 20
	integer :: ixq
	real(kind = 8) :: xqmin
	real(kind = 8) :: xqmax
	real(kind = 8) :: dxq
    	complex(kind = 8), dimension(:, :, :, :), allocatable :: Chi_0_charge_q
	integer :: Nenergy = 600
	real(kind = 8), dimension(:), allocatable :: energy
	real(kind = 8) :: energyUpper
	real(kind = 8) :: energyLower
	real(kind = 8) :: denergy
    	Integer :: L_dim = 4
	real(kind = 8) :: eps_f, chem
	real(kind = 8) :: Rv = 0.955_dp
	complex(kind = 8), dimension(:, :, :), allocatable :: Chi_int
	real(kind = 8), dimension(:), allocatable :: xqarray
	complex(kind = 8), dimension(:, :), allocatable :: f_z, g_z
	integer :: i, j, mu, nu, ku, lu
	integer :: nw
	real(kind = 8) :: re, imag
	complex(kind = 8) :: alpha_n, beta_n, gamma_n
	real(kind = 8) :: x1
	complex(kind = 8), dimension(:, :), allocatable :: Z_hlp
	complex(kind = 8) :: czero = dcmplx(0, 0)
    	integer :: ienergy
	complex(kind = 8) :: f
	real(kind = 8), parameter :: pi = acos(-1.0_dp)

	narg = command_argument_count()
    	if (narg .ne. 3) then
		write(*, *) "Argument number is wrong."
		write(*, *) "sigma_file is the first argument"
		write(*, *) "beta is the second argument, mu_file is the third argument. "
		stop
	endif
	call getarg(1, buffer)
    	read(buffer, *) sigma_file
    	call getarg(2, buffer)
	read(buffer, *) beta
	call getarg(3, buffer)
    	read(buffer, *) mu_file

	Niom = max(int(Niom_factor*beta), NiomMin)
    	Niom2 = max(int(beta*Niom2_factor), 20)
    	allocate(xiom(Niom), xiom2(-Niom+1:Niom))

    	allocate(xqarray(nxq))
    	xqmin = -0.999_dp
	xqmax = -xqmin
	dxq = (xqmax - xqmin)/dble(nxq-1)
    	do ixq = 1, nxq
		xqarray(ixq) = xqmin + (ixq - 1)*dxq
	enddo

	Allocate(Chi_int(nxq, L_dim, L_dim))
    	allocate(f_z(norb, norb), g_z(norb, norb))
    	allocate(sigma(Niom, norb, norb))
    	allocate(sigma_temp(-Niom+1:Niom, norb, norb))
    	allocate(Chi_0_charge_q(nxq, -Niom2+1:Niom2, L_dim, L_dim))
    	allocate(Z_hlp(L_dim, L_dim))
    	allocate(energy(Nenergy))

    	energyUpper = 20.0_dp
	energyLower = -energyUpper
    	denergy = (energyUpper - energyLower)/dble(Nenergy)
    	do ienergy = 1, Nenergy
		energy(ienergy) = energyLower + (ienergy - 0.5_dp)*denergy
	enddo
    	
	open(unit = 17, file = sigma_file, action = "read")
	do i = 1, norb
	do j = 1, norb
		read(17, *) row, col
		do nw = 1, Niom
			read(17, *) xiom(nw), re, imag
			sigma(nw, row, col) = dcmplx(re, imag)
		enddo
	enddo
	enddo
	close(17)

    	do i = 1, norb
	do j = 1, norb
		do nw  = 1, Niom
			sigma_temp(nw, i, j) = sigma(nw, i, j)
    			sigma_temp(-nw+1, i, j) = conjg(sigma(nw, i, j))
		enddo
	enddo
	enddo

	do nw = -Niom+1, Niom
		xiom2(nw) = dble(2*(nw-1) + 1)*pi/beta
	enddo

    	open(unit = 19, file = mu_file, action = "read")
	read(19, *) chem
	read(19, *) eps_f
	read(19, *) eps_f
	close(19)

        if(.true.) then
    	do ixq = 1, nxq
	do nw = -Niom2 + 1, Niom2
		x1 = xqarray(ixq)
    		alpha_n = ii*xiom2(nw) - (eps_f - chem) - sigma_temp(nw, 2, 2)
    		beta_n = ii*xiom2(nw) + chem - sigma_temp(nw, 1, 1)
    		gamma_n = beta_n - (Rv + sigma_temp(nw, 1, 2))*(Rv + sigma_temp(nw, 2, 1))/alpha_n
		Z_hlp = czero
		if (.true.) then
		do ienergy = 1, Nenergy
			f_z(1, 1) = f(gamma_n, energy(ienergy), x1)
    			f_z(1, 2) = (Rv + sigma_temp(nw, 1, 2))/alpha_n*f(gamma_n, energy(ienergy), x1)
    			f_z(2, 1) = (Rv + sigma_temp(nw, 2, 1))/alpha_n*f(gamma_n, energy(ienergy), x1)
    			f_z(2, 2) = 1.0_dp/alpha_n*(1.0_dp + &
				&(Rv + sigma_temp(nw, 1, 2))*(Rv + sigma_temp(nw, 2, 1))/&
				&alpha_n*f(gamma_n, energy(ienergy), x1))
    			g_z(1, 1) = 1.0_dp/(gamma_n - energy(ienergy))
    			g_z(1, 2) = (Rv + sigma_temp(nw, 1, 2))/alpha_n*(1.0_dp/(gamma_n - energy(ienergy)))
    			g_z(2, 1) = (Rv + sigma_temp(nw, 2, 1))/alpha_n*(1.0_dp/(gamma_n - energy(ienergy)))
    			g_z(2, 2) = (beta_n - energy(ienergy))/(alpha_n*(gamma_n - energy(ienergy)))
    			i = 0
			do nu = 1, norb
			do mu = 1, norb
				i = i + 1
				j = 0
				do ku = 1, norb
				do lu = 1, norb
					j = j + 1
					Z_hlp(i, j) = Z_hlp(i, j) + denergy*(1.0_dp/sqrt(pi))&
					&*exp(-energy(ienergy)**2)*f_z(nu, ku)*g_z(lu, mu)
				enddo
				enddo
			enddo
			enddo
		enddo
		endif
		do i = 1, L_dim
		do j = 1, L_dim
			Chi_0_charge_q(ixq, nw, i, j) = -2.0_dp*Z_hlp(i, j)
		enddo
		enddo
	enddo
	enddo
	close(13)
	endif

    	Chi_int = czero
	do ixq = 1, nxq
		do i = 1, L_dim
		do j = 1, L_dim
			do nw = -Niom2+1, Niom2
				Chi_int(ixq, i, j) = Chi_int(ixq, i, j) + Chi_0_charge_q(ixq, nw, i, j)
			enddo
		enddo
		enddo
	enddo

	Chi_int = Chi_int/beta

	if (.false.) then
	open(unit = 13, file = "Chi_int", action = "write")
	do ixq = 1, nxq
		write(13, *) xqarray(ixq)
		do i = 1, L_dim
		do j = 1, L_dim
			write(13, *) i, "  ", j, "  ", Chi_int(ixq, i, j)
		enddo
		enddo
	enddo
	close(13)
    	endif

	write(*, *) beta
	do ixq = 1, nxq
		write(*, *) xqarray(ixq) 
    		do i = 1, L_dim
		do j = 1, L_dim
			write(*, *) i, "  ", j, "  ", Chi_int(ixq, i, j)
		enddo
		enddo
	enddo

    	Deallocate(Chi_int)
    	deallocate(f_z, g_z)
    	deallocate(sigma, sigma_temp)
    	deallocate(Chi_0_charge_q)
    	deallocate(xiom, xiom2)
    	deallocate(Z_hlp)
    	deallocate(energy)	
 end program main
