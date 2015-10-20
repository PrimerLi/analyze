program main
implicit none
	complex(kind = 8), dimension(:, :, :, :), allocatable :: matrix
	complex(kind = 8), dimension(:, :, :), allocatable :: eigenvalues 
	integer :: i, j, row, col, i_sus, ixq, N_sus, nxq
	integer :: L_dim, Ndim, Niom2, Niom
	integer :: matrixDimension
	real(kind = 8), dimension(:), allocatable :: xq
	integer :: mu, nu
	real(kind = 8) :: a, b
	complex(kind = 8) :: trace
	complex(kind = 8), dimension(:, :), allocatable :: tempMatrix
	complex(kind = 8), dimension(:), allocatable :: tempVector, VL
	complex(kind = 8), dimension(:, :), allocatable :: rightEigenvectors
	integer :: info, lwork
	complex(kind = 8), dimension(:), allocatable :: work
	real(kind = 8), dimension(:), allocatable :: rwork
	complex(kind = 8), dimension(:, :, :, :), allocatable :: U

	N_sus = 3
	nxq = 2
	L_dim = 4
	open(unit = 17, file = "Niom", action = "read")
		read(17, *) Niom
		read(17, *) Niom2
	close(17)
	Ndim = 2*Niom2
	matrixDimension = L_dim*Ndim
	lwork = 2*matrixDimension
	allocate(work(lwork))
    	allocate(rwork(2*matrixDimension))
	allocate(matrix(N_sus, nxq, matrixDimension, matrixDimension))
    	allocate(eigenvalues(N_sus, nxq, matrixDimension))
    	allocate(xq(nxq))
    	allocate(tempMatrix(matrixDimension, matrixDimension))
    	allocate(tempVector(matrixDimension), VL(matrixDimension))
    	allocate(rightEigenvectors(matrixDimension, matrixDimension))
    	allocate(U(N_sus, nxq, matrixDimension, matrixDimension))

    	open(unit = 13, file = "M_regularized", action = "read")
	do i_sus = 1, N_sus
		read(13, *) i
		do ixq = 1, nxq
			read(13, *) xq(ixq)
    			do row = 1, matrixDimension
			do col = 1, matrixDimension
				read(13, *) mu, nu
				read(13, *) a, b
				matrix(i_sus, ixq, row, col) = dcmplx(a, b)
			enddo
			enddo
		enddo
	enddo
	close(13)

    	do i_sus = 1, N_sus
		do ixq = 1, nxq
			do i = 1, matrixDimension
				do j = 1, matrixDimension
					tempMatrix(i, j) = matrix(i_sus, ixq, i, j)
				enddo
			enddo
			call zgeev("N", "V", matrixDimension, tempMatrix, matrixDimension, tempVector, VL, matrixDimension, rightEigenvectors, matrixDimension, work, lwork, rwork, info)	
    			do i = 1, matrixDimension
				eigenvalues(i_sus, ixq, i) = tempVector(i)
			enddo
			do i = 1, matrixDimension
			do j = 1, matrixDimension
				U(i_sus, ixq, i, j) = rightEigenvectors(i, j)
			enddo
			enddo
		enddo
	enddo

	open(unit = 17, file = "eigenvalues.txt", action = "write")
	do i_sus = 1, N_sus
		write(17, *) i_sus
		do ixq = 1, nxq
			write(17, *) xq(ixq)
			do i = 1, matrixDimension
				write(17, *) i, "    ", eigenvalues(i_sus, ixq, i)
			enddo
		enddo
	enddo
	close(19)

	open(unit = 19, file = "rightEigenvectors.txt", action = "write")
	do i_sus = 1, N_sus
		write(19, *) i_sus
		do ixq = 1, nxq
			write(19, *) xq(ixq)
    			do i = 1, matrixDimension
				write(19, *) eigenvalues(i_sus, ixq, i)
				do j = 1, matrixDimension
					write(19, *) j, "  ", U(i_sus, ixq, i, j) 
				enddo
			enddo
		enddo
	enddo
	close(19)

    	deallocate(matrix, eigenvalues, xq)
    	deallocate(tempMatrix)
    	deallocate(tempVector, VL)
    	deallocate(rightEigenvectors)
    	deallocate(work, rwork)
    	deallocate(U)
end program main

