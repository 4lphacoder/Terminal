let removeBtns = document.getElementsByClassName('remove-enrollments-btn');
let batchName = document.getElementById('batch-name').innerHTML.split('_');
let programme = batchName[0];
let branch = batchName[1];
let section = batchName[2];
let year_of_pass = batchName[3];
let deleteAllBtn = document.getElementById('delete-batch-btn');
let submit = document.getElementById('submit-enrollment-btn');
let enrollment = document.getElementById('enrollment-insertion-field');

// EVENT LISTENERS ---START
for(let itr = 0; itr < removeBtns.length ; itr++){
    removeBtns[itr].addEventListener('click', () => {
        enrollment = removeBtns[itr].getAttribute('name');
        jsonBody = {
            'programme':programme,
            'branch':branch,
            'section':section,
            'year_of_pass':year_of_pass,
            'enrollment':[ enrollment ]
        }
        fetch('/admin/remove', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            credentials: 'same-origin',
            body: JSON.stringify( jsonBody )
        }).then( response => response.json())
        .then( response => {
            if( response['status'][enrollment] == 220 ){
                removeBtns[itr].parentElement.parentElement.style.display = 'none';
            }
        } )
    })
}

// EVENT LISTENERS ---END

// EVENT LISTENERS ---START
deleteAllBtn.addEventListener('click', ()=> {
    jsonBody = {
        'programme':programme,
        'branch':branch,
        'section':section,
        'year_of_pass':year_of_pass
    }
    fetch('/admin/remove_all',{
        method: 'POST',
        headers: { 'Content-Type':'application/json','Accept':'application/json'},
        credentials: 'same-origin',
        body: JSON.stringify( jsonBody )
    }).then( response => response.json())
    .then( response => {
        console.log(response)
        // if( response.status == 212){
        //     console.log('deleted batch');
        // }
    })
})
// EVENT LISTENERS ---END

// EVENT LISTENERS ---START
submit.addEventListener('click', ()=> {
    console.log(programme);
    console.log(branch);
    console.log(section);
    console.log(year_of_pass);
    console.log(enrollment.value);
    jsonBody = {
            'programme':programme,
            'branch':branch,
            'section':section,
            'year_of_pass':year_of_pass,
            'enrollment':[ enrollment.value ] 
        }
    fetch('/admin/insert',{
        method: 'POST',
        headers: { 'Content-Type':'application/json','Accept':'application/json'},
        credentials: 'same-origin',
        body: JSON.stringify( jsonBody )
    }).then(response => response.json())
    .then( response => {
            console.log(response)
            
    })
})
