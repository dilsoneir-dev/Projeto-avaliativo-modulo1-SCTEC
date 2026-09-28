-- ====================================================================
-- Projeto Avaliativo - Módulo 1 (SCTEC / SENAI)
-- Query 1: Salários por Departamento e Cargo
-- Objetivo: Analisar a distribuição salarial dos funcionários relacionando
--           departamentos e cargos (JOBS).
-- ====================================================================

SELECT 
    e.EMPLOYEE_ID,
    e.FIRST_NAME,
    e.LAST_NAME,
    e.SALARY,
    d.DEPARTMENT_ID,
    d.DEPARTMENT_NAME,
    j.JOB_ID,
    j.JOB_TITLE,
    j.MIN_SALARY,
    j.MAX_SALARY
FROM HR.EMPLOYEES e
LEFT JOIN HR.DEPARTMENTS d 
    ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
LEFT JOIN HR.JOBS j 
    ON e.JOB_ID = j.JOB_ID
WHERE e.DEPARTMENT_ID IS NOT NULL
ORDER BY e.SALARY DESC;
