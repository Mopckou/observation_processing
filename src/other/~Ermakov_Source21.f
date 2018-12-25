        program aprox
        !EXTERNAL DIFF_APROX
        REAL A(61,4), U(61,4), V(61,4), SIGMA(4), WORK(4), C(4), RELEER
        REAL SIGMA1, TAU, Y(3401), Delta_T, t_nul, T(3401), TEST, width
        REAL BEST, C_BEST(4), COUNT, WORK_ARRAY(3, 4, 3401)
        REAL WIDTH_ARRAY(3), DIFF_APROX
        INTEGER I, IERR, J, M, N, NM, m_begin, m_end, M_OBSH, windows
        INTEGER COUNT_OSHIBOK
        LOGICAL IMPORTANT_SECTION, FLAG
        real B(3401,2)
c
        NM = 3401
        M = 3401
        N = 4
        CALL readArray(B, 3401, 2)
c        PRINT*, B(3401,1)
        print *, 'TEST'
        DO 10 I = 1, NM
           T(I) = B(I, 1)
           Y(I) = B(I, 2)
10      CONTINUE
        RELEER = 0.000001
        WORK_ARRAY = 0
        WIDTH_ARRAY(1) = 26.
        WIDTH_ARRAY(2) = 27.
        WIDTH_ARRAY(3) = 28.
        COUNT_OSHIBOK = 0
        !width = 27.
        !t_nul = 133.
        !I = 100
        windows = 61
        !windows = 39
        BEST = -1.
        M_OBSH = M - windows
        COUNT = 0.
        DO 20 K = 1, SIZE(WIDTH_ARRAY)
        width = WIDTH_ARRAY(K)
        !PRINT*, width
        DO 21 I = 1, M_OBSH
           COUNT = COUNT + 1
           diff = 0.
           m_begin = I
           m_end =I + windows ! ���ᨬ��쭮� ���-�� �� ���ᨢ� ��� ����� ���樨, ��� ���ᨢ ���� ���� ���஥ ��������� �� �ᥬ� ���ᨢ� �������, ��������� � 蠣�� 1
           t_nul = I + (windows/2.)
           WORK_ARRAY(K,1,I) = T(I)
           WORK_ARRAY(K,3,I) = t_nul
           !PRINT*, 1.
           !PRINT*, SIZE(T(m_begin:m_end))
           !PRINT*, windows
        CALL CALC_MATR_PLANE(A, T(m_begin:m_end), windows, t_nul, width)
        CALL SVD(windows,windows,N,A,SIGMA,.TRUE.,U,.TRUE.,V,IERR, WORK)
            IF (IERR.NE.0) Then
            WORK_ARRAY(K,2,I) = -1.
            COUNT_OSHIBOK = COUNT_OSHIBOK + 1!write
            GO TO 21 !PRINT*, 'oshibka' !
            ENDIF  !PRINT*, SIGMA
        CALL CALC_COEFF(Y(m_begin:m_end),U,V,SIGMA,C,windows,N,RELEER) ! Y(m_begin:m_end) ��१�� ���� �� ���ᨢ� ������� (��� ����殮���)
           diff = DIFF_APROX(A, Y(m_begin:m_end), C, windows, N) ! �業�� ��பᨬ�樨
           WORK_ARRAY(K,2,I) = diff
           FLAG = IMPORTANT_SECTION(Y(m_begin:m_end), windows, 20, 1)
           IF(FLAG .EQV. .TRUE.) THEN
           WORK_ARRAY(K,4,I) = 1.
           ELSE
           WORK_ARRAY(K,4,I) = 0.
           ENDIF
           PRINT*, diff,  C(4), t_nul, FLAG
           !PRINT*, C(4)

21      CONTINUE
20      CONTINUE
        PRINT*, 'count'
        !PRINT*, WORK_ARRAY(2,2,:)
        PRINT*, 'otchet'
        !PRINT*, BEST
        PRINT*, 'oshibki'
        PRINT*, COUNT_OSHIBOK
        CALL ANALIZE_WORK_ARRAY(WORK_ARRAY, SIZE(WIDTH_ARRAY), M)!,  )
        pause
        stop
        end
        
        SUBROUTINE ANALIZE_WORK_ARRAY(WORK_ARRAY, K, N)!, RESULT)
        REAL WORK_ARRAY(K,3,N), MIDDLE_RESULT(K, N)!, RESULT(N)
        REAL FILTR_MIN
        INTEGER K, N, COUNT_MIN, L

        MIDDLE_RESULT = 0.
        DO 30 J = 1, K
        FILTR_MIN = -1.
           DO 31 I = 1, N    ! ��宦����� �������쭮�� �������, ᠬ� ��������� �� ��ﬠ� ᮢ������� � �஢��� �㬠 3.0 V. ��� ���� �᪫����
           diff = WORK_ARRAY(J, 2, I)
           IF (FILTR_MIN .EQ. -1.) Then
              FILTR_MIN = diff
           ELSE IF ((diff .GT. 0.) .and. (FILTR_MIN .GT. diff)) THEN
                FILTR_MIN = diff
           ENDIF
31         CONTINUE
           PRINT*, 'filtr'
           PRINT*, FILTR_MIN
           
           COUNT_MIN = 0
           DO 32 I = 1, N    ! ������ ᪮�쪮 ����砥��� �� ���祭��
           diff = WORK_ARRAY(J, 2, I)
                IF (FILTR_MIN .EQ. WORK_ARRAY(J, 2, I)) Then
                   COUNT_MIN = COUNT_MIN + 1
                ENDIF
32         CONTINUE
!           PRINT*, WORK_ARRAY(J, 2, 1)
           PRINT*, COUNT_MIN
           IF (COUNT_MIN .GT. 10) THEN
           PRINT*, COUNT_MIN
                   WHERE (WORK_ARRAY(J, 2, :) .EQ. FILTR_MIN) ! ��饭�� ���ᨢ� �� ������� ���������� ���祭��
                         WORK_ARRAY(J, 2, :) = 0.
                   ENDWHERE
           ENDIF

           L = 1
           DO 33 I = 1, N    ! ��室�� ����⢨⥫쭮 ��������� ���祭��
           diff = WORK_ARRAY(J, 2, I)
           IF ((diff .GT. 0.) .and. (diff .LT. 1.)) THEN
                MIDDLE_RESULT(J, L) = diff
                L = L + 1
           ENDIF
33         CONTINUE
            
            
30      CONTINUE
        !PRINT*, WORK_ARRAY(3,2,:)
        PRINT*, 'hello'
        !PRINT*, MIDDLE_RESULT(1,:)
        RETURN
        END
        
        
        SUBROUTINE CALC_MATR_PLANE(A, T, M, t_nul, width)
        REAL T(M), t_nul, width, A(M, 4)
        INTEGER M, TEST
        !PRINT*, 'OGO'
        !TEST = 0
        DO 70 I = 1, M
           A(I, 1) = 1.
           A(I, 2) = Delta_T(T(I), t_nul)
           A(I, 3) = Delta_T(T(I), t_nul) * Delta_T(T(I), t_nul)
           A(I, 4) = Right_Angled(T(I), t_nul, width)
           !TEST = TEST + 1
70      CONTINUE
        !PRINT*, SIZE(T)
        !PRINT*, 'colvo'
        !PRINT*, TEST
        RETURN
        END

CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
CCCCC   �㭪�� ��थ����� ���⪠ �� ���஬ �ந�室�� �⪫��.        CCCCC
CCCCC   �ᯮ������ ��� �����஢���� ���⪮� 䮭�, ��� ���������  CCCCC
CCCCC   �����쭠� ��பᨬ���, ��� �� ᠬ�� ���� ���� 䮭 ��砩��    CCCCC
CCCCC   ᮢ������ � �㭪樥�                                            CCCCC
CCCCC   Y - ���ᨢ � ��室�묨 ����묨, WINDOWS - ࠡ�祥 ���� (���� �� CCCCC
CCCCC   �ᥬ� ����� ���������), ANGLE - 㣮� ��������� ��䨪�        CCCCC
CCCCC   �� ���஬ ��⠥� ���⮪ ������. (㣮� ��������� �����   CCCCC
CCCCC   �⭮�⥫쭮 ��㣮� �窨), D - ���-�� �祪 ���஥ ��।�塞  CCCCC
CCCCC   �᫨ ���-�� �祪 10, � D - 2, � ࠡ�稩 ���ᨢ MASS �㤥� ��  �����
CCCCC   5 ������⮢. � ������ ������� �㤥� �।��� 2 �祪. �����     �����
CCCCC   ���� �ࠢ����� 㣫� ����� 5 �窠��, �᫨ ����� �� 1 � �� 2,    �����
CCCCC   㣮� ����� ��������� � ANGLE, � ���⮪ ������, � ᪮॥  �����
CCCCC   �ᥣ� �� �⮬ ���⪥ �⪫��                                    CCCCC
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
        LOGICAL FUNCTION IMPORTANT_SECTION(Y, WINDOWS, ANGLE, D)
        INTEGER WINDOWS, D, I, J, M, C, GET_ANGLE, ANGLE, VAL
        REAL Y(WINDOWS), MASS, ksin, kcos
        LOGICAL FLAG
        ALLOCATABLE MASS(:)
        FLAG = .FALSE.
        M = WINDOWS/D ! �.�. M - integer, ���㣫���� �� ������� �ந�室�� ��⮬���᪨
        ALLOCATE(MASS(M))
        !PRINT*, 'M', M
        !PRINT*, 'Y', Y
        MASS = 0.
        C = 0
        DO 10 I = 1, M
           DO 20 J = 1, D
              C = C + 1
              MASS(I) = MASS(I) + Y(C)
              !PRINT*, Y(C)
20         CONTINUE
           MASS(I) = MASS(I)/D
10      CONTINUE
        !PRINT*, MASS
        DO 30 I = 1, (M-1)
           ksin = MASS(I+1) - MASS(I)
           kcos = D
           !PRINT*, 'iter',I, 'ksin=', ksin, 'kcos=',kcos
           VAL = GET_ANGLE(ksin, kcos)
           !PRINT*, 'val=', VAL
           IF (VAL .GT. ANGLE) THEN
              FLAG = .TRUE.
              GOTO 40
           ENDIF
30      CONTINUE
40      DEALLOCATE(MASS)
        !PRINT*, FLAG
        IMPORTANT_SECTION = FLAG
        RETURN
        END
CCCCCC �㭪�� �����頥� 㣮� ����� �窠��                            �����
        INTEGER FUNCTION GET_ANGLE(ksin, kcos) ! �����頥� integer, ��ࠢ������ ⮫쪮 � integer
        INTEGER ANS
        REAL ksin, kcos
        REAL (kind=8) PI, gip
        PI = ACOS(-1._8)
        GIP = SQRT(ksin**2 + kcos**2)
        ARCCOS = ACOS(kcos/GIP)
        GET_ANGLE = (ARCCOS * 180.)/PI
        RETURN
        END

CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
CCCCC   �㭪�� ������ �����⭮�� ���� �� �㬬� �����⮢ ���燐�   CCCCC
CCCCC   �ᯮ������ ��� �業�� ��பᨬ�樨                            CCCCC
CCCCC   � - ����� �����, Y - ���ᨢ ��室��� ������, � - ���ᨢ ����� CCCCC
CCCCC   M - ������⢮ �祪 ��१�� �������, N - ����-�� ����       CCCCC
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

        REAL FUNCTION DIFF_APROX(A, Y, C, M, N)
        INTEGER I, J, M, N
        REAL A(M, N), Y(M), C(N), RSQ, RI, T
        
        RSQ = 0.
        DO 80 I = 1, M
           RI = 0.
           DO 90 J = 1, N
              RI = RI + C(J) * A(I, J)
90         CONTINUE
           RSQ = RSQ + (RI - Y(I))**2
80      CONTINUE
        !PRINT*, SQRT(RSQ)
        DIFF_APROX = SQRT(RSQ)
        return
        end

CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
CCCCC   �㭪�� ������ �����樥�⮢ �(N)                             CCCCC
CCCCC                                                                   CCCCC
CCCCC   Y - ���ᨢ ��室��� ������, � - ���ᨢ �����                    CCCCC
CCCCC   M - ������⢮ �祪 ��१�� �������, N - ����-�� ����       CCCCC
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

        SUBROUTINE CALC_COEFF(Y, U, V, SIGMA, C, M, N, RELEER)
        INTEGER M, N, I, J
        REAL SIGMA(N), C(N), Y(M), V(M, N), U(M, N)
        REAL TAU, SIGMA1, RELEER, S
        SIGMA1 = 0.
        DO 30 J = 1, N
           IF (SIGMA(J).GT.SIGMA1)SIGMA1 = SIGMA(J)
           C(J) = 0.
 30     CONTINUE
        TAU = RELEER * SIGMA1
c
        DO 60 J = 1,N
           IF(SIGMA(J).LE.TAU)GO TO 60
           S = 0.
           DO 40 I = 1, M
              S = S+U(I,J)*Y(I)
 40        CONTINUE
           S = S/SIGMA(J)
           DO 50 I = 1, N
              C(I) = C(I) + S*V(I,J)
 50        CONTINUE
 60     CONTINUE
        !PRINT*, C
        RETURN
        END
        

        REAL FUNCTION Delta_T(t, t_nul)
        REAL t, t_nul
             Delta_T = t - t_nul
        RETURN
        END
        
        REAL FUNCTION Right_Angled(t, t_nul, width)
        REAL t, t_nul, width
        IF  (t >= (t_nul-(width/2.)) .and. t <= (t_nul+(width/2.))) THEN
            Right_Angled = 1.
        ELSE
            Right_Angled = 0.
        END IF
        RETURN
        END
        
        SUBROUTINE readArray(A, n, m)

        integer i,j,n,m,curColumn
        real A(n,m)

c        n=266
c        m=2

c        allocate(A(n,m))

        open(10,file='data.txt')
        do 3333 i=1,n
        read(10,*)(A(i,j),j=1,m)
3333     continue
        close(10)

c        curColumn=2
c        x=A(:,curColumn)
         PRINT*, 'OK'
c        write(*,"(f6.2,1x)")x
c        PRINT*, A(266,1)
c        pause
c        stop
        return
        end
        
         SUBROUTINE SVD(NM,M,N,A,W,MATU,U,MATV,V,IERR,RV1)
	INTEGER*2 I,J,K,L,M,N,II,I1,KK,K1,LL,L1,MN,NM,ITS,IERR
c     *  IERRNM
c           Attention, Otladka !: Perewozu iz form.par.
c           wse massiwi A,U,V,W,RV1   =>   w Common !
c           + int=>int*2, real=>real*4
c           + isklyuchayu NM iz opisaniya i form.par.tolko.
c2018-02-18: Vse massivy iz <common> perevedeny obratno v
c           formaljnie parametry SVD(..) -- dlya ispoljzovaniya
c           A.Ermakovim v programme obrabotki dannih KRT.
c           => proveritj SVD po tekstu Forsajta esche raz !!!
c
	REAL*4 A(NM,N), W(N), U(NM,N), V(NM,N), RV1(N)
	REAL*4 C, F, G, H, S, X, Y, Z, SCALE, ANORM
	LOGICAL MATU, MATV
c        common /svd12/ A,U,V,W,RV1
	IERR=0
	DO 100 I=1,M
	DO 100 J=1,N
	U(I,J)=A(I,J)
  100	CONTINUE
	G=0.0
	SCALE=0.0
	ANORM=0.0
	DO 300 I=1,N
	   L=I+1
	   RV1(I)=SCALE*G
	   G=0.0
	   S=0.0
	   SCALE=0.0
	   IF (I .GT .M) GO TO 210
	   DO 120 K=I,M
  120	   SCALE=SCALE+ABS(U(K, I))
	   IF(SCALE .EQ. 0.0) GO TO 210
	   DO 130 K=I, M
	          U(K, I)=U(K, I)/SCALE
                  S=S+U(K,I)**2
  130	   CONTINUE
	   F=U(I, I)
	   G=-SIGN(SQRT(S), F)
	   H=F*G-S
	   U(I, I)=F-G
	   IF (I .EQ. N) GO TO 190
	   DO 150 J=L, N
	      S=0.0
       DO 140 K=I, M
  140	      S=S+U(K, I)*U(K, J)
	      F=S/H
	      DO 150 K=I, M
	         U(K, J)=U(K, J)+F*U(K, I)
  150	   CONTINUE
  190	   DO 200 K=I, M
  200	   U(K, I)=SCALE*U(K, I)
  210	   W(I)=SCALE*G
	   G=0.0
 	   S=0.0
	   SCALE=0.0
	   IF(I .GT. M .OR. I .EQ. N) GO TO 290
	   DO 220 K=L, N
  220	   SCALE=SCALE+ABS(U(I,K))
	   IF(SCALE. EQ. 0.0) GO TO 290
	   DO 230 K=L, N
	      U(I, K)=U(I, K)/SCALE
	      S=S+U(I, K)**2
  230	   CONTINUE
	   F=U(I, L)
	   G=-SIGN(SQRT(S),F)
	   H=F*G-S
	   U(I,L)=F-G
	   DO 240 K=L, N
  240	   RV1(K)=U(I, K)/H
	   IF (I .EQ. M) GO TO 270
  	   DO 260 J=L, M
	      S=0.0
	      DO 250 K=L, N
  250	      S=S+U(J, K)*U(I, K)
	      DO 260 K=L, N
		 U(J, K)=U(J, K)+S*RV1(K)
  260	   CONTINUE
  270    DO 280 K=L, N
  280	   U(I, K)=SCALE*U(I, K)
  290	   ANORM=AMAX1(ANORM, ABS(W(I))+ABS(RV1(I)))
  300	CONTINUE
	   IF (.NOT.MATV) GO TO 410
	   DO 400 II=1, N
	      I=N+1-II
	      IF (I.EQ.N) GO TO 390
            IF (G.EQ.0.0) GO TO 360
	      DO 320 J=L, N
  320	      V(J, I)=(U(I, J)/U(I, L))/G
	      DO 350 J=L, N
		 S=0.0
		 DO 340 K=L, N
  340		 S=S+U(I, K)*V(K, J)
		 DO 350 K=L, N
		    V(K, J)=V(K, J)+S*V(K, I)
  350	   CONTINUE
  360	   DO 380 J=L, N
	      V(I, J)=0.0
	      V(J, I)=0.0
  380	   CONTINUE
  390	   V(I, I)=1.0
	   G=RV1(I)
	   L=I
  400	   CONTINUE
  410    IF (. NOT. MATU) GOTO 510
	MN=N
	IF (M .LT. N) MN=M
	DO 500 II=1, MN
	   I=MN+1-II
	   L=I+1
	   G=W(I)
	   IF (I .EQ. N) GO TO 430
	   DO 420 J=L, N
  420	   U(I, J)=0.0
  430	   IF(G. EQ. 0.0) GO TO 475
	   IF(I. EQ. MN) GO TO 460
	   DO 450 J=L, N
	      S=0.0
            DO 440 K=L, M
  440	      S=S+U(K, I)*U(K, J)
	      F=(S/U(I, I))/G
	      DO 450 K=I, M
		 U(K, J)=U(K, J)+F*U(K, I)
  450	   CONTINUE
  460	   DO 470 J=I, M
  470	   U(J, I)=U(J, I)/G
	   GO TO 490
  475	   DO 480 J=I, M
  480	   U(J, I)=0.0
  490    U(I, I)=U(I,I)+1.0
  500	CONTINUE
  510	DO 700 KK=1, N
	   K1=N-KK
	   K=K1+1
	   ITS=0
  520	   DO 530 LL=1, K
	      L1=K-LL
	      L=L1+1
	      IF (ABS(RV1(L))+ANORM .EQ. ANORM) GO TO 565
	      IF (ABS(W(L1))+ANORM .EQ. ANORM) GO TO 540
  530	   CONTINUE
  540	   C=0.0
	   S=1.0
	   DO 560 I=L, K
	      F=S*RV1(I)
	      RV1(I)=C*RV1(I)
	      IF (ABS(F)+ANORM .EQ. ANORM) GO TO 565
	      G=W(I)
	      H=SQRT(F*F+G*G)
	      W(I)=H
	      C=G/H
	      S=-F/H
	      IF(.NOT. MATU) GO TO 560
	      DO 550 J=1, M
		 Y=U(J, L1)
		 Z=U(J,I)
		 U(J, L1)=Y*C+Z*S
  		 U(J, I)=-Y*S+Z*C
  550	CONTINUE
  560	   CONTINUE
  565	   Z=W(K)
	   IF(L .EQ. K) GO TO 650
	   IF(ITS .EQ. 30) GO TO 1000
	   ITS=ITS+1
	   X=W(L)
	   Y=W(K1)
	   G=RV1(K1)
	   H=RV1(K)
	   F=((Y-Z)*(Y+Z)+(G-H)*(G+H))/(2.0*H*Y)
	   G=SQRT(F*F+1.0)
	   F=((X-Z)*(X+Z)+H*(Y/(F+SIGN(G, F))-H))/X
	   C=1.0
	   S=1.0
	   DO 600 I1=L, K1
            I=I1+1
	      G=RV1(I)
	      Y=W(I)
	      H=S*G
	      G=C*G
	      Z=SQRT(F*F+H*H)
	      RV1(I1)=Z
	      C=F/Z
	      S=H/Z
	      F=X*C+G*S
	      G=-X*S+G*C
	      H=Y*S
	      Y=Y*C
	      IF (.NOT. MATV) GO TO 575
	      DO 570 J=1, N
	         X=V(J, I1)
		 Z=V(J, I)
		 V(J, I1)=X*C+Z*S
		 V(J, I)=-X*S+Z*C
  570	      CONTINUE
  575	      Z=SQRT(F*F+H*H)
	      W(I1)=Z
	      IF (Z.EQ. 0.0) GO TO 580
	      C=F/Z
	      S=H/Z
  580	      F=C*G+S*Y
	      X=-S*G+C*Y
	      IF (.NOT. MATU) GO TO 600
	      DO 590 J=1, M
		 Y=U(J, I1)
		 Z=U(J, I)
	         U(J, I1)=Y*C+Z*S
		 U(J, I)=-Y*S+Z*C
  590	      CONTINUE
  600	   CONTINUE
	   RV1(L)=0.0
	   RV1(K)=F
	   W(K)=X
	   GO TO 520
  650	   IF (Z. GE. 0.0) GO TO 700
	   W(K)=-Z
	   IF(.NOT. MATV) GO TO 700
	   DO 690 J=1, N
  690	   V(J, K)=-V(J, K)
  700	CONTINUE
	GO TO 1001
 1000	IERR=K
 1001	RETURN
	END