        program aprox
        REAL A, U, V, SIGMA, WORK, C, RELEER, SIGMA1, TAU, Y, T
        REAL Delta_T, t_nul, width, DIFF_APROX, AMPLITUDE
        REAL AMP, GET_AVERAGE
        INTEGER I, IERR, J, M, N, NM, m_begin, m_end, M_OBSH, windows
        INTEGER NAll, F ! количество всех точек в файле
        LOGICAL IMPORTANT_SECTION, FLAG
        ALLOCATABLE A(:,:),U(:,:),V(:,:),WORK(:),C(:),SIGMA(:),Y(:),T(:)
        READ(*,*) F
        READ(*,*) width
        READ(*,*) M ! размер окна
!        PRINT*, M
        READ(*,*) N
!        PRINT*, N
        READ(*,*) NAll
        ALLOCATE (A(M, N),U(M, N),V(M, N),WORK(N),C(N),SIGMA(N))
        ALLOCATE (Y(NAll), T(NAll))
        NM = M
        RELEER = 0.000001

        DO 10 I = 1, NAll
        READ(*,*) T(I)
!           PRINT*, T(I)
10      CONTINUE
        DO 15 I = 1, NAll
           READ(*,*) Y(I)
!           PRINT*, Y(I)
15      CONTINUE






        windows = M
        
        M_OBSH = NAll - (windows - 1)
        !PRINT*, windows
        !PRINT*, 'Nall', NAll

        !PRINT*, M_OBSH
        DO 21 I = 1, M_OBSH
           diff = 0.
           m_begin = I
           m_end = I + windows - 1 ! максимальное кол-во эл массива для одной итерации, этот массив есть окно которое двигается по всему массиву наблюдений, двигается с шагом 1
           t_nul = T(I) + (windows/2.)
        !PRINT*, 1
        CALL CALC_MATR_PLANE(F,A,T(m_begin:m_end),windows,t_nul,width)
        !print*, 'ta;', T(m_begin:m_end)
        !print*, A
        CALL SVD(windows,windows,N,A,SIGMA,.TRUE.,U,.TRUE.,V,IERR, WORK)
        !print*, SIGMA
        CALL CALC_COEFF(Y(m_begin:m_end),U,V,SIGMA,C,windows,N,RELEER) ! Y(m_begi34e5a23n:m_end) вырезка окна из массива наблюдений (ось напряжения)
           diff = DIFF_APROX(A, Y(m_begin:m_end), C, windows, N) ! оценка апроксимации

           !FLAG = .True.!IMPORTANT_SECTION(Y(m_begin:m_end), windows, 10, 1)
           AMP = AMPLITUDE(A,Y(m_begin:m_end),C,windows,N,t_nul,width)

           PRINT*, C, diff, t_nul, AMP
21      CONTINUE
        !CALL ANALIZE_WORK_ARRAY(WORK_ARRAY, SIZE(WIDTH_ARRAY), M)!,  )
        DEALLOCATE (A, U, V, WORK, C, SIGMA, Y, T)
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
           DO 31 I = 1, N    ! нахождение минимального элемента, самый минимальный это прямая совпадающая с уровнем шума 3.0 V. Его надо исключить
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
           DO 32 I = 1, N    ! подсчет сколько встречается это значение
           diff = WORK_ARRAY(J, 2, I)
                IF (FILTR_MIN .EQ. WORK_ARRAY(J, 2, I)) Then
                   COUNT_MIN = COUNT_MIN + 1
                ENDIF
32         CONTINUE
!           PRINT*, WORK_ARRAY(J, 2, 1)
           PRINT*, COUNT_MIN
           IF (COUNT_MIN .GT. 10) THEN
           PRINT*, COUNT_MIN
                   WHERE (WORK_ARRAY(J, 2, :) .EQ. FILTR_MIN) ! очищение массива от неверных минимальных значений
                         WORK_ARRAY(J, 2, :) = 0.
                   ENDWHERE
           ENDIF

           L = 1
           DO 33 I = 1, N    ! находим действительно минимальные значения
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
        
        
        SUBROUTINE CALC_MATR_PLANE(FUNC, A, T, M, t_nul, width)
        REAL T(M), t_nul, width, A(M, 4), Right_Angled, Gauss
        INTEGER M, TEST, FUNC
        !PRINT*, 'OGO'
        !TEST = 0
        DO 70 I = 1, M
           A(I, 1) = 1.
           A(I, 2) = Delta_T(T(I), t_nul)
           A(I, 3) = Delta_T(T(I), t_nul) * Delta_T(T(I), t_nul)
           IF (FUNC .EQ. 0) THEN
           A(I, 4) = Right_Angled(T(I), t_nul, width)
           ELSE
           A(I, 4) = Gauss(T(I), t_nul, width)
           ENDIF
           !TEST = TEST + 1
70      CONTINUE
        !PRINT*, SIZE(T)
        !PRINT*, 'colvo'
        !PRINT*, TEST
        RETURN
        END

CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
CCCCC   Функция опрделения участка на котором происходит отклик.        CCCCC
CCCCC   Используется для игнорирования участков фона, где присутствует  CCCCC
CCCCC   идеальная апроксимация, хотя на самом деле лишь фон случайно    CCCCC
CCCCC   совпадает с функцией                                            CCCCC
CCCCC   Y - массив с исходными данными, WINDOWS - рабочее окно (идет по CCCCC
CCCCC   всему участку наблдения), ANGLE - угол изменения графика        CCCCC
CCCCC   при котором считаем участок интересным. (угол изменения одной   CCCCC
CCCCC   относительно другой точки), D - кол-во точек которое усредняем  CCCCC
CCCCC   Если кол-во точек 10, и D - 2, то рабочий массив MASS будет из  ССССС
CCCCC   5 элементов. В каждом элементе будет среднее 2 точек. Далее     ССССС
CCCCC   идет сравнение угла между 5 точками, если между эл 1 и эл 2,    ССССС
CCCCC   угол больше заданного в ANGLE, то участок интересный, и скорее  ССССС
CCCCC   всего на этом участке отклик                                    CCCCC
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
        LOGICAL FUNCTION IMPORTANT_SECTION(Y, WINDOWS, ANGLE, D)
        INTEGER WINDOWS, D, I, J, M, C, GET_ANGLE, ANGLE, VAL
        REAL Y(WINDOWS), MASS, ksin, kcos
        LOGICAL FLAG
        ALLOCATABLE MASS(:)
        FLAG = .FALSE.
        M = WINDOWS/D ! т.к. M - integer, округление от деление происходит автоматически
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
        DO 25 I = 1, M
        DO 30 J = 1, M
           ksin = MASS(I) - MASS(J)
           kcos = D
           !PRINT*, 'iter',I, 'ksin=', ksin, 'kcos=',kcos
           VAL = GET_ANGLE(ksin, kcos)
           !PRINT*, 'val=', VAL
           IF (VAL .GT. ANGLE) THEN
              FLAG = .TRUE.
              GOTO 40
           ENDIF
30      CONTINUE
25      CONTINUE
40      DEALLOCATE(MASS)
        !PRINT*, FLAG
        IMPORTANT_SECTION = FLAG
        RETURN
        END
CCCCCC Функция возвращает угол между точками                            ССССС
        INTEGER FUNCTION GET_ANGLE(ksin, kcos) ! возвращает integer, приравнивать только к integer
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
CCCCC   Функция подсчета квадратного корня из суммы квадратов невязок   CCCCC
CCCCC   Используется для оценки апроксимации                            CCCCC
CCCCC   А - матрица плана, Y - массив исходных данных, С - массив коэфф CCCCC
CCCCC   M - количество точек отрезка наблюдения, N - колл-во коэф       CCCCC
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
CCCCC   Функция подсчета коэффициентов С(N)                             CCCCC
CCCCC                                                                   CCCCC
CCCCC   Y - массив исходных данных, С - массив коэфф                    CCCCC
CCCCC   M - количество точек отрезка наблюдения, N - колл-во коэф       CCCCC
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

        REAL FUNCTION AMPLITUDE(A, Y, C, M, N, t_nul, width)
        INTEGER I, J, M, N
        REAL A(M, N), Y(M), C(N), Y_NEW(M), POINT, T, t_nul, width
        REAL BEGIN_AVERAGE, END_AVERAGE, GET_AVERAGE, MAX, Gauss

        DO 70 I = 1, M
           POINT = 0.
           DO 71 J = 1, N
              POINT = POINT + C(J) * A(I, J)
71         CONTINUE
           Y_NEW(I) = POINT
70      CONTINUE
        !PRINT*, 'LOL'
        BEGIN_AVERAGE = GET_AVERAGE(Y_NEW(:10), 10)
        END_AVERAGE = GET_AVERAGE(Y_NEW(M-10+1:), 10)
        !PRINT*, 'LOL@'
        
        MAX = C(1) + C(4) * Gauss(t_nul, t_nul, width)
        AMPLITUDE = MAX - ((BEGIN_AVERAGE + END_AVERAGE)/2.)
        return
        end
        
        REAL FUNCTION GET_AVERAGE(MASS, N)
        INTEGER I, N
        REAL MASS(N), SUMM

        SUMM = 0.
        DO 72 I = 1, N
        SUMM = SUMM + MASS(I)
72      CONTINUE

        GET_AVERAGE = SUMM / N
        return
        end
        

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
        
        REAL FUNCTION Gauss(t, t_nul, width)
        REAL t, t_nul, width
        REAL (kind=8) PI, x, Lambda, coeff
        PI = ACOS(-1._8)
        coeff = 1/(width*SQRT(2*PI))
        x = Lambda(t, t_nul, width)
        Gauss = coeff * exp(x)
        RETURN
        END
        
        REAL FUNCTION Lambda(t, t_nul, width)
        REAL t, t_nul, width
        Lambda = -(t-t_nul)*(t-t_nul)/100.*width*width
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
