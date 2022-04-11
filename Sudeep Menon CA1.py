'''
Create a class Employee, and create and test a function to compute net pay from payment, work and tax credit information.

Employee should have the following attributes:
StaffID, LastName, FirstName, RegHours, HourlyRate, OTMultiple, TaxCredit, StandardBand,

For Example:

jg= Employee(12345,'Green','Joe', 37, 16, 1.5, 72, 710)

Create a method computePayment in class Employee which takes HoursWorked and date as input, and returns a payment information dictionary as follows: (if jg is an Employee object for worker Joe Green)

We will assume a standard rate of 20% and a higher rate of 40%, and that PRSI at 4% is not subject to allowances. (we will ignore USC etc.)

>>>jg.computePayment(42, '31/10/2021')

{'name': 'Joe Green', 'Date':'31/10/2021', 'Regular Hours Worked':37,'Overtime Hours Worked':5,'Regular Rate':16,'Overtime Rate':24, 'Regular Pay':592,'Overtime Pay':120,'Gross Pay':712, 'Standard Rate Pay':710,'Higher Rate Pay':2, 'Standard Tax':142,'Higher Tax':0.8,'Total Tax':142.8,'Tax Credit':72, 'Net Tax':70.8, 'PRSI': 28.48,'Net Deductions':99.28, 'Net Pay': 612.72}

Test your class and method thoroughly, and at a minimum include test cases testing the following:

Net pay cannot exceed gross pay 

#TestMethod

def testNetLessEqualGross(self):
  e=Employee(#Joe Green's Information)
  pi=e.computePayment(1,'31/10/2021')
  self.assertLessEqual(pi['Net Pay'],pi['Gross Pay'])

Overtime pay or overtime hours cannot be negative.

Regular Hours Worked cannot exceed hours worked

Higher Tax cannot be negative.

Net Pay cannot be negative.
'''
 
import unittest

class Employee:
    def __init__(self, staff_id, last_name, first_name, regHours, hourlyRate, otMultiple, taxCredit, standardBand) :
        self.__staffID = staff_id
        self.__lastName = last_name
        self.__firstName = first_name
        self.__regHours = regHours
        self.__hourlyRate = hourlyRate
        self.__otMultiple = otMultiple
        self.__taxCredit = taxCredit
        self.__standardBand = standardBand

    def computePayment(self, hoursWorked, date):
        pay_details={}
        pay_details['name'] = self.__firstName+" "+self.__lastName
        pay_details['Date'] = date
        
        # Checking if Working hours is Negative. If Negative then raise a value error.
        if(hoursWorked < 0):
            raise ValueError("Hours worked Cannot be less than Zero")

        # Calculate Regular Hours Worked
        # Checking if Regular Hours exceed hours worked. If exceed then raise a value error.
        if(self.__regHours >= hoursWorked):
           raise ValueError("Regular Hours Cannot be exceed Hours worked")
        pay_details['Regular Hours Worked'] = self.__regHours
        pay_details['Overtime Hours Worked'] = 0
        
        # Calculate Overtime hours worked
        if(hoursWorked >= self.__regHours):    
            pay_details['Overtime Hours Worked'] = hoursWorked - self.__regHours
        else:
            pay_details['Regular Hours Worked'] = hoursWorked

        #Calculate Overtime Rate
        pay_details['Regular Rate'] = self.__hourlyRate
        pay_details['Overtime Rate'] = self.__hourlyRate * self.__otMultiple

        #Calculate Regular pay, Overtime Pay and Gross Pay
        pay_details['Regular Pay'] = pay_details['Regular Hours Worked'] * pay_details['Regular Rate']
        pay_details['Overtime Pay'] = pay_details['Overtime Hours Worked'] * pay_details['Overtime Rate']
        pay_details['Gross Pay'] = pay_details['Regular Pay'] + pay_details['Overtime Pay']
        
        #Calculate Higher Rate Pay
        pay_details['Standard Rate Pay'] = self.__standardBand
        if(pay_details['Overtime Hours Worked'] == 0):
            pay_details['Higher Rate Pay'] = 0
        else:
            pay_details['Higher Rate Pay'] = pay_details['Gross Pay'] - pay_details['Standard Rate Pay']
        
        # check if Higher Rate Pay is negative
        if(pay_details['Higher Rate Pay'] <= 0):
            pay_details['Higher Rate Pay'] = 0
            # raise ValueError("Higher Rate Pay Cannot be Negative") #If negative then Raise value Error

        if(pay_details['Gross Pay'] <= pay_details['Standard Rate Pay']):
            pay_details['Standard Tax'] = round(((pay_details['Gross Pay']*20)/100),2)
        else:
            pay_details['Standard Tax'] = round(((pay_details['Standard Rate Pay']*20)/100),2)
        pay_details['Higher Tax'] = round(((pay_details['Higher Rate Pay']*40)/100),2)
        #check if Higher Tax is negative, If negative then Raise value Error
        # if(pay_details['Higher Tax'] <= 0):
        #     raise ValueError("Higher Tax Pay Cannot be Negative")
        
        #Calculate Taxes
        pay_details['Total Tax'] = pay_details['Standard Tax'] + pay_details['Higher Tax']
        pay_details['Tax Credit'] = self.__taxCredit
        pay_details['Net Tax'] = round(pay_details['Total Tax'] - pay_details['Tax Credit'],2)
        pay_details['PRSI'] = round(((pay_details['Gross Pay']*4)/100),2)

        #Calculate Net Deductions and Net Pay
        pay_details['Net Deductions'] = round(pay_details['Net Tax'] + pay_details['PRSI'],2)
        pay_details['Net Pay'] = round(pay_details['Gross Pay'] - pay_details['Net Deductions'],2)
        # check if Net Pay is negative, If negative then Raise value Error
        if(pay_details['Net Pay'] <= 0):
            raise ValueError("Net Pay Cannot be Negative")
        
        #print(pay_details)
        return pay_details

class Unit_test(unittest.TestCase):
    # Net Pay should be less than Gross Pay.
    def testNetLessEqualGross(self):
        e=Employee(12345,'Green','Joe', 37, 16, 1.5, 72, 710)
        cp=e.computePayment(47, '31/10/2021')
        self.assertLessEqual(cp['Net Pay'],cp['Gross Pay'])

    # Overtime pay or overtime hours cannot be negative.
    def testOvertimeNegative(self):
        e=Employee(12345,'Green','Joe', 37, 16, 1.5, 72, 710)
        with self.assertRaises(ValueError):
            # if Work Hours is less than zero then Raise a Value error
            e.computePayment(-40,'31/10/2021')

    # Regular Hours Worked cannot exceed hours worked
    def testRegHrLessEqualHrWrked(self):
        e=Employee(12345,'Green','Joe', 37, 16, 1.5, 72, 710)
        # if Work Hours is less than Regular work hours then Raise a Value error
        with self.assertRaises(ValueError):
            e.computePayment(30,'31/10/2021')
            
    # Higher Tax cannot be negative.
    def testHigherTaxNegative(self):
        e=Employee(12345,'Green','Joe', 37, 16, 1.5, 72, 710)
        cp=e.computePayment(38, '31/10/2021')
        # Higher tax should be greater than or equal to zero
        self.assertGreaterEqual(cp['Higher Tax'],0)

        # if Higher tax is negative then should Raise a Value error
        #with self.assertRaises(ValueError):
        #    e.computePayment(38,'31/10/2021')

    # Net Pay cannot be negative.
    def testNetPayNegative(self):
        e=Employee(12345,'Green','Joe', 37, 16, 1, 5, 710)
        cp=e.computePayment(38, '31/10/2021')
        # Net Pay should be greater than or equal to zero
        self.assertGreaterEqual(cp['Net Pay'],0)
        
        # if Net Pay is negative then should Raise a Value error
        # with self.assertRaises(ValueError):
        #     e.computePayment(40,'31/10/2021')

unittest.main(argv=['ignored'], exit=False)