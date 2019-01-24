//SAMPLE 1
// status 2 - additional details required
// export const GenerateFamilyCodeJson = {
//   'message': 'Additional details required',
//   'sibWOPC': [
//       {
//           'dob': '2008-11-04 00:00:00',
//           'fname': 'Steven',
//           'lname': 'Abdelkader',
//           'paymentcode': null,
//           'selected': true,
//           'studentid': '8401750809813'
//       },
//       {
//         'dob': '2008-11-04 00:00:00',
//         'fname': 'Maria',
//         'lname': 'Abdelkader',
//         'paymentcode': null,
//         'selected': false,
//         'studentid': '8401750809814'
//     },
//       {
//         'dob': '2008-11-04 00:00:00',
//         'fname': 'Daniel',
//         'lname': 'Abdelkader',
//         'paymentcode': null,
//         'selected': false,
//         'studentid': '8401750809815'
//     }

//   ],
//   'sibWPC': null,
//   'status': 2
// }


// status 2 - additional details required
// export const GenerateFamilyCodeJson = {
//   'message': 'Additional details required',
//   'sibWOPC': [
//       {
//           'dob': '2008-11-04 00:00:00',
//           'fname': 'Steven',
//           'lname': 'Abdelkader',
//           'paymentcode': null,
//           'selected': true,
//           'studentid': '8401750809813'
//       },
//       {
//         'dob': '2008-11-04 00:00:00',
//         'fname': 'Maria',
//         'lname': 'Abdelkader',
//         'paymentcode': null,
//         'selected': false,
//         'studentid': '8401750809814'
//     },
//       {
//         'dob': '2008-11-04 00:00:00',
//         'fname': 'Daniel',
//         'lname': 'Abdelkader',
//         'paymentcode': null,
//         'selected': false,
//         'studentid': '8401750809815'
//     }

//   ],
//   'sibWPC': [
//       {
//           'dob': '2008-11-04 00:00:00',
//           'fname': 'Youssef',
//           'lname': 'Abdelkader',
//           'paymentcode': 'CD_01',
//           'selected': false,
//           'studentid': 'ST_ID_01'
//       }
//   ],
//   'status': 2
// }


  //SAMPLE 2
  // Status 1 - code generated successfuly 

  export const GenerateFamilyCodeJson = {
    'status' : 1,
    'additionaldetails': null,
    'message': 'BXCCAD'
  }


  //SAMPLE 3
  // status 0 - unable to generate due to internal error.

  // export const GenerateFamilyCodeJson = {
  //   'status' : 0,
  //   'additionaldetails': null,
  //   'message': 'Unable to generate the code'
  // }