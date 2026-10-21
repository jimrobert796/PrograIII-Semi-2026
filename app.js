document.addEventListener("DOMContentLoaded", (events) => {
  const mnxImpuestos = document.getElementById("mnxImpuestos");
  if (mnxImpuestos) {
    // Delegación de eventos: escuchamos clics en el contenedor
    mnxImpuestos.addEventListener("click", (e) => {
      // Buscamos el elemento más cercano que tenga el atributo data-form
      const target = e.target.closest("[data-form]");
      if (target) {
        e.preventDefault();
        let form = target.dataset.form;
        cargarForm(form);
      }
    });
  }
});

function guardarUsuario(accion) {
    const datos = {
        modulo: 'usuario',
        accion: accion,
        idUsuario: $('#idUsuario').val(),
        usuario: $('#usuario').val(),
        clave: $('#clave').val(),
        nombre: $('#nombre').val(),
        direccion: $('#direccion').val(),
        telefono: $('#telefono').val()
    };

    fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
        alert('Respuesta del servidor: ' + data.msg);
        if (data.msg === 'ok') {
            cargarForm('busqueda_usuarios');
            buscarUsuarios();
        }
    })
    .catch(error => console.error('Error:', error));
}

function buscarUsuarios() {
    const buscar = $('#buscarUsuario').val();
    fetch(`/usuarios?buscar=${buscar}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.json();
    })
    .then(datos => {
        let html = '';
        if (datos && datos.length > 0) {
            datos.forEach(u => {
                html += `<tr>
                    <td>${u.idUsuario}</td>
                    <td>${u.usuario}</td>
                    <td>${u.nombre}</td>
                    <td>${u.telefono}</td>
                    <td>
                        <button onclick="editarUsuario(${u.idUsuario}, '${u.usuario}', '${u.clave}', '${u.nombre}', '${u.direccion}', '${u.telefono}')">Editar</button>
                    </td>
                </tr>`;
            });
        } else {
            html = '<tr><td colspan="5" style="text-align:center;">No se encontraron usuarios</td></tr>';
        }
        $('#tablaUsuarios').html(html);
    })
    .catch(error => {
        console.error('Error:', error);
        $('#tablaUsuarios').html('<tr><td colspan="5" style="text-align:center; color:red;">Error al cargar los datos</td></tr>');
    });
}

function editarUsuario(id, user, clave, nombre, dir, tel) {
    cargarForm('usuarios');
    $('#idUsuario').val(id);
    $('#usuario').val(user);
    $('#clave').val(clave);
    $('#nombre').val(nombre);
    $('#direccion').val(dir);
    $('#telefono').val(tel);
}

function cargarForm(form, callback) {
    if ($(`#${form} > form`).length <= 0 || $(`#${form}`).html().trim() === "") {
    fetch(`/vistas?form=${form}`)
      .then((response) => response.text())
      .then((ventana) => {
        $(`#${form}`).html(ventana).draggable();
        cerrarVentana();
        if (callback) callback();
      })
      .catch((error) => console.error("Error al cargar el formulario:", error));
  } else {
    $(`#${form}`).show();
  }
}
function cerrarVentana() {
  $(".btn-close")
    .off("click")
    .on("click", (e) => {
      e.preventDefault();
      let form = e.target.dataset.form;
      $(`#${form}`).hide();
    });
}
