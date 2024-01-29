from flask import render_template, request, redirect, url_for, flash
from api.reservations import reservations
from api.reservations.controllers import get_reservations, get_reservation, create_reservation, delete_reservation, update_reservation
from api.auth.decorators import login_required 
from api.equipment.controllers import get_equipment_list
from api.timeslots.controllers import get_timeslots

import time 

###############################
# RESERVATION VIEW FUNCTIONS ##
###############################


@reservations.get('/')
def index():
    search = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    if search is not None: 
        r = get_reservations(search=search)
        count = len(r)
        if request.headers.get('HX-Trigger') == 'search':
            time.sleep(2)
            return render_template('reservations/rows.html', reservations=r, count=count)
    else:
        r = get_reservations()
        count = len(r)
    return render_template('reservations/index.html', reservations=r, page=page, count=count)

@reservations.get('/count')
def count():
    time.sleep(2)
    count = len(get_reservations())
    return "(" + str(count) + " total Reservations)"

@reservations.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        r = create_reservation(request)
        if r is None:
            flash('Reservation not created!', 'error')
            return render_template('reservations/create.html')
        flash('Reservation created successfully!', 'success')
        return redirect(url_for('reservations.index'), 303)
    e = get_equipment_list()
    ts = get_timeslots()
    return render_template('reservations/create.html', equipment=e, timeslots=ts)

@reservations.route('/<int:id>', methods=['GET', 'PUT'])
@login_required
def update(id: int):
    if request.method == 'PUT':
        r, msg = update_reservation(id=id, request=request)
        if r is None:
            flash(msg or 'Uh-oh! Something went wrong while trying to update', 'error')
            r = get_reservation(id)  # Get the reservation again for rendering the template
            e = get_equipment_list()
            ts = get_timeslots()
            return render_template('reservations/update.html', reservation=r, equipment=e, timeslots=ts, status=303)
        flash('Reservation updated successfully!', 'success')
        return redirect(url_for('reservations.index'), 303)
    else:
        r = get_reservation(id)
        e = get_equipment_list()
        ts = get_timeslots()
        return render_template('reservations/update.html', reservation=r, equipment=e, timeslots=ts)


@reservations.delete('/<int:id>')
@login_required
def delete(id: int):
    delete_reservation(id)
    flash('Reservation deleted successfully!', 'success')
    return redirect(url_for('reservations.index'), 303)
