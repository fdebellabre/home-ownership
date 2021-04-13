import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def monthly_payments(e, n, r):
    """
    Computes the constant monthly payments of a loan

    :param e: (float) amount borrowed
    :param n: (float) loan duration in years
    :param r: (float) interest rate
    :return L: (np.array) left to pay
    :return M: (np.array) monthly payments
    :return R: (np.array) monthly reimbursement
    :return I: (np.array) monthly interest
    """
    n = n*12
    r = pow(1+r,1/12)-1
    N = np.arange(n+1)
    M = np.append(0, np.repeat(e*(r/(1-pow(1+r,-n))), n))
    R = M/pow(1+r,n-N+1)
    L = e-np.cumsum(R)
    I = M-R
    return(L, R, M, I)

def ownership_cost(loyer, prix, apport, n, r, i=None, notaire=0.08, agence=0.05, foncier=2000, tapprec=0.001):
    """
    Computes when ownership becomes more profitable than rental

    :param loyer: (float) monthly rent
    :param prix: (float) price of the good
    :param apport: capital contribution of the buyer
    :param n: (int) loan duration in years
    :param r: (float) loan interest rate
    :param i: (float) alternative interest rate if investing
    :param notaire: (float) solicitor fee (rate)
    :param agence: (float) agency fee (rate)
    :param foncier: (float) property tax
    :param tapprec: (float) appreciation rate of the good
    :return diff: (np.array) difference between rental cost and ownership cost
    :return m: (float) monthly payments
    :return icost: (np.array) total interest cost of the loan
    :return threshold: (float) month after which ownership is more profitable
    """
    emprunt = prix*(1+notaire)*(1+agence)-apport
    
    L, R, M, I = monthly_payments(emprunt, n, r)
    
    n = n*12
    r = pow(1+r,1/12)-1
    tapprec = pow(1+tapprec,1/12)-1
    i = r if i==None else pow(1+i,1/12)-1

    MAX = max(n+1, 1200)
    L = np.append(L, np.zeros(MAX-len(L)))
    R = np.append(R, np.zeros(MAX-len(R)))
    M = np.append(M, np.zeros(MAX-len(M)))
    I = np.append(I, np.zeros(MAX-len(I)))
    N = np.arange(MAX)

    # Scenario 1: renting
    loyer = np.append(0, np.repeat(loyer, MAX-1))
    invest_apport = apport*((pow(1+i,N)-1))
    invest_savings = np.cumsum((M-loyer)*(pow(1+i,N)-1))
    loss_rent = np.cumsum(loyer) - invest_apport - invest_savings

    # Scenario 2: buying at time 0 then selling
    invest_savings = np.cumsum(np.where(N-n>0, np.max(M), 0)*(pow(1+i, N-n)-1))
    selling_price = prix*pow(1+tapprec, N)
    loss_buysell = apport - selling_price + L + np.cumsum(M) + N*foncier/12 - invest_savings

    diff = loss_rent - loss_buysell

    threshold = np.argmax(diff>=0)
    if np.max(diff)<0: threshold=np.inf
    return(diff, np.max(M), np.sum(I), threshold)
