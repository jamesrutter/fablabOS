from flask import render_template, request, redirect, url_for, flash
from api.reservations import reservations
from api.reservations.controllers import get_reservations, get_reservation, create_reservation, delete_reservation, update_reservation
from api.auth.decorators import login_required 
from api.equipment.controllers import get_equipment_list
from api.timeslots.controllers import get_timeslots

###############################
# RESERVATION VIEW FUNCTIONS ##
###############################


@reservations.get('/')
def index():
    r = get_reservations()
    return render_template('reservations/index.html', reservations=r)


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
