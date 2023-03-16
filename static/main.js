const GACHA_RESULT = [];
const HEADERS = ['池子', '幸运等级', '出目', '稀有度', '名称', '职业', '属性加成', '描述'];
const HEADERS_INVENTORY = ['名称', '稀有度', '职业', '属性加成', '效果', '操作'];
const KEYS = ['pool', 'success_level', 'roll', 'rarity', 'name', 'class', 'stats', 'effect'];
const SINGLE_GACHA_PRICE = { 'minion': 7, 'boss': 10 };
const MINION_POOL_PRICE = 7;
let poolSelection;

document.addEventListener('DOMContentLoaded', function () {
    const singleBtn = document.querySelector('#btn-single');
    const tenTimesBtn = document.querySelector('#btn-ten-times');
    const submitBtn = document.querySelector('#submit-btn');
    const addEquipmentBtn = document.querySelector('#add-equipment-btn');
    const updateGoldBtn = document.querySelector('#update-gold-btn');
    const updateLuckBtn = document.querySelector('#update-luck-btn');

    if (singleBtn) {
        singleBtn.addEventListener('click', single);
    }

    if (tenTimesBtn) {
        tenTimesBtn.addEventListener('click', tenTimes);
    }

    if (submitBtn) {
        submitBtn.addEventListener('click', addEquipment);
    }

    if (addEquipmentBtn) {
        addEquipmentBtn.addEventListener('click', addEquipmentToPlayer);
    }

    if (updateGoldBtn) {
        updateGoldBtn.addEventListener('click', updateGold);
    }

    if (updateLuckBtn) {
        updateLuckBtn.addEventListener('click', updateLuck);
    }
    populateDropdowns();
});

function single() {
    poolSelection = document.getElementById('inlineFormCustomSelectPref').value;
    checkGold(poolSelection, 1);
}

function tenTimes() {
    poolSelection = document.getElementById('inlineFormCustomSelectPref').value;
    checkGold(poolSelection, 10);
}

function callGacha(poolSelection, times) {
    $.ajax({
        url: '/gacha',
        type: 'POST',
        data: { pool: poolSelection, times: times },
        success(batch) {
            GACHA_RESULT.unshift(batch.results);
            updateGachaTable();
            $('#main-table').css('visibility', 'visible');
            updateGoldNavbar(batch.gold);
        },
        error() {
            console.log('Failed to call /gacha');
        },
    });
}

function addEquipment() {
    $.ajax({
        url: "/add_equipment_admin",
        type: "POST",
        data: $("#equipment-form").serialize(),
        success: function (data) {
            // Clear form inputs after successful submission
            $('#equipment-form').find('input, textarea').val('');
        },
        error: function (xhr, status, error) {
            console.log(error);
        }
    });
}

function addEquipmentToPlayer() {
    // populate dropdowns
    // handle add equipment button click
    $('#add-equipment-btn').on('click', function (event) {
        var userId = $('#user-select').val();
        var equipmentId = $('#equipment-select option:selected').val(); // use .data() to get the equipment id
        $.ajax({
            url: '/add_equipment_to_userid',
            method: 'POST',
            data: {
                'user_id': userId,
                'equipment_id': equipmentId
            },
            success: function (data) {
                // success message or table update here
                console.log('Equipment added to user successfully');
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });    });
}

function checkGold(poolSelection, times) {
    $.ajax({
        url: '/get_gold',
        type: 'GET',
        success(user) {
            if (user.gold >= SINGLE_GACHA_PRICE[poolSelection] * times) {
                callGacha(poolSelection, times);
            } else {
                alert('没有足够的金币哦');
            }
        },
        error(xhr, status, error) {
            console.log(error);
        },
    });
}

function updateGold() {
    var userId = $('#user-select').val();
    var goldAmount = $('#gold-input').val();
    $.ajax({
        url: '/update_gold',
        type: 'POST',
        data: { user_id: userId, amount: goldAmount },
        success(response) {
            if (userId === sessionUserId) {
                updateGoldNavbar(response.gold);
            }
        },
        error(xhr, status, error) {
            console.log(`Error updating gold: ${status} ${error}`);
        },
    });
}

function updateLuck() {
    var userId = $('#user-select').val();
    var luckAmount = $('#luck-input').val();
    $.ajax({
        url: '/update_luck',
        type: 'POST',
        data: { user_id: userId, luck: luckAmount },
        success(response) {
            if (userId === sessionUserId) {
                updateLuckNavbar(response.luck);
            }
        },
        error(xhr, status, error) {
            console.log(`Error updating luck: ${status} ${error}`);
        },
    });
}

function updateGoldNavbar(amount) {
    $('.user-gold').text(amount);
}

function updateLuckNavbar(luck) {
    $('.user-luck').text(luck);
}
// function to populate user and equipment dropdowns
function populateDropdowns() {
    $.ajax({
        url: '/get_users_all',
        method: 'GET',
        success: function (data) {
            // populate user dropdown
            var userDropdown = $('#user-select');
            userDropdown.empty();
            userDropdown.append($('<option>', {
                value: '',
                text: '选择用户'
            }));
            $.each(data.users, function (i, user) {
                userDropdown.append($('<option>', {
                    value: user.user_id,
                    text: user.username
                }));
            });
        },
        error: function (xhr, status, error) {
            console.log(error);
        }
    });

    $.ajax({
        url: '/get_equipment_all',
        method: 'GET',
        success: function (data) {
            // populate equipment dropdown
            var equipmentDropdown = $('#equipment-select');
            equipmentDropdown.empty();
            equipmentDropdown.append($('<option>', {
                value: '',
                text: '选择装备',
            }));
            $.each(data.equipment, function (i, equipment) {
                equipmentDropdown.append($('<option>', {
                    value: equipment.ids,
                    text: equipment.ids + equipment.name,
                }));
            });
        },
        error: function (xhr, status, error) {
            console.log(error);
        }
    });
}

function updateGachaTable() {
    // Destroy existing DataTable if it exists
    if ($.fn.DataTable.isDataTable('#gacha-result-table')) {
        $('#gacha-result-table').DataTable().destroy();
    }

    // update gacha results
    let table = `<table class="table table-striped table-hover table-sm " id="gacha-result-table">`;
    table += "<thead><tr>";
    for (const item of HEADERS) {
        table += `<th class="header text-nowrap" scope="col">${item}</th>`;
    }
    table += "</tr></thead><tbody>";

    for (const batch of GACHA_RESULT) {
        for (const item of batch) {
            table += "<tr>";
            for (const info of KEYS) {
                table += `<td>${item[info]}</td>`;
            }
            table += "</tr> ";
        }
    }
    table += "</tbody></table>";
    document.getElementById("main-table").innerHTML = table;

    // Re-initialize the DataTable
    $('#gacha-result-table').DataTable();
}


function initializeTable(selector, ajaxUrl, columns, rowClickHandler) {
    const table = $(selector).DataTable({
        ajax: {
            url: ajaxUrl,
            dataSrc: 'inventory',
        },
        columns: columns,
    });

    if (rowClickHandler) {
        $(selector + ' tbody').on('click', '.sell-btn', rowClickHandler);
    }

    return table;
}

$(document).ready(function () {
    const inventoryColumns = [
        { data: 'equipment.name' },
        { data: 'equipment.rarity' },
        { data: 'equipment.class' },
        { data: 'equipment.stats' },
        { data: 'equipment.effect' },
        { data: 'timestamp' },
        {
            data: 'equipment_id',
            render: function (data, type, row) {
                return `<button class="sell-btn" data-item-id="${data}">出售</button>`
                    + `&nbsp;<button class="remove-btn" data-item-id="${data}">摧毁</button>`;
            },
        },
    ];

    function inventoryRowClickHandler(event, clickedElement, inventoryTable) {
        // prevent the default action of the button, which is to submit the form
        event.preventDefault();
        const itemId = $(clickedElement).data('item-id');
        $.ajax({
            url: '/sell',
            type: 'POST',
            data: { 'equipment_id': itemId },
            success: function (data) {
                // update the inventory table
                inventoryTable.ajax.reload(null, false);
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    }

    function inventoryRemoveRowClickHandler(event, clickedElement, inventoryTable) {
        // prevent the default action of the button, which is to submit the form
        event.preventDefault();
        const itemId = $(clickedElement).data('item-id');
        $.ajax({
            url: '/remove_equipment_from_userid',
            type: 'POST',
            data: { 'equipment_id': itemId, 'target_id': sessionUserId }, // Use the user_id from the session
            success: function (data) {
                // update the inventory table
                inventoryTable.ajax.reload(null, false);
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    }
    const inventoryTable = initializeTable('#inventory', '/getinventory', inventoryColumns, null);
    $('#inventory tbody').on('click', '.sell-btn', function (event) {
        inventoryRowClickHandler(event, this, inventoryTable);
    });
    $('#inventory tbody').on('click', '.remove-btn', function (event) {
        inventoryRemoveRowClickHandler(event, this, inventoryTable);
    });
    const inventoryAllColumns = [
        { data: 'user_id' },
        { data: 'equipment.name' },
        { data: 'equipment.rarity' },
        { data: 'equipment.class' },
        { data: 'equipment.stats' },
        { data: 'equipment.effect' },
        { data: 'timestamp' },
        {
            data: null,
            render: function (data, type, row) {
                return `<button class="sell-btn" data-item-id="${data.equipment_id}" data-target-id="${data.user_id}">移除</button>`;
            },
        },
    ];

    const inventoryAllRowClickHandler = function (event, clickedElement, inventoryTableALL) {
        // handle click event for the sell button in the inventory-all table
        event.preventDefault();
        var item_id = $(clickedElement).data('item-id');
        var target_id = $(clickedElement).data('target-id');
        $.ajax({
            url: '/remove_equipment_from_userid',
            type: 'POST',
            data: { 'equipment_id': item_id, 'target_id': target_id },
            success: function (data) {
                // update the inventory table
                inventoryTableAll.ajax.reload(null, false);
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    };

    const inventoryTableAll = initializeTable('#inventory-all', '/getinventoryall', inventoryAllColumns, null);
    $('#inventory-all tbody').on('click', '.sell-btn', function (event) {
        inventoryAllRowClickHandler(event, this, inventoryTableAll);
    });
});

$(document).ready(function () {
    // get equipment items and populate them in the table
    var equipmentTable = $('#items-all').DataTable({
        ajax: {
            url: '/get_equipment_all',
            dataSrc: 'equipment'
        },
        columns: [
            { data: 'ids' },
            { data: 'category' },
            { data: 'name' },
            { data: 'innerid' },
            { data: 'rarity' },
            { data: 'class' },
            { data: 'cost' },
            { data: 'stats' },
            { data: 'effect' },
            {
                data: null,
                render: function (data, type, row) {
                    // add the equipment_id to the button's data attributes
                    return '<button class="sell-btn" data-item-id="' + data.ids + '">移除</button>';
                }
            }
        ]
    });

    // handle click event for the sell button
    $('#items-all tbody').on('click', '.sell-btn', function (event) {
        // prevent the default action of the button, which is to submit the form
        event.preventDefault();
        var item_id = $(this).data('item-id');
        console.log(this)
        $.ajax({
            url: '/remove_equipment_from_list',
            type: 'POST',
            data: { 'equipment_id': item_id },
            success: function (data) {
                // update the equipment table
                equipmentTable.ajax.reload(null, false);
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });
});