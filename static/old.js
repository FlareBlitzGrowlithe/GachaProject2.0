
//import $ from 'jquery';
var gachaResult = [];
var HEADERS = ["池子", "幸运等级", "出目", "稀有度", "名称", "职业", "属性加成", "描述",];
var HEADERS_INVENTORY = ["名称", "稀有度", "职业", "属性加成", "效果", "操作"];
var KEYS = ["pool", "success_level", "roll", "rarity", "name", "class", "stats", "effect",]
var SINGLE_GACHA_PRICE = { "minion": 7, "boss": 10 };
var MINION_POOL_PRICE = 7;
var PoolSelection;


function Single() {
    PoolSelection = document.getElementById("inlineFormCustomSelectPref").value;
    CheckGold(PoolSelection, 1);
}

function TenTimes() {
    PoolSelection = document.getElementById("inlineFormCustomSelectPref").value;
    CheckGold(PoolSelection, 10);
}

// call gacha api
function CallGacha(PoolSelection, times) {
    $.ajax({
        url: "/gacha",
        type: "POST",
        data: { pool: PoolSelection, times: times },
        success: function (batch) {
            gachaResult.unshift(batch.results);
            UpdateGachaTable();
            $('#main-table').css('visibility', 'visible');
            UpdateGoldWebPage(batch.gold);
        },
        error: function () {
            console.log("Failed to call /gacha");
        }
    });
    // TODO: 大失败提示信息栏
}

function SellItem(equipment_id) {
    $.ajax({
        url: "/sell",
        type: "POST",
        data: { "equipment_id": equipment_id },
        success: function (results) {
            // Display the results in a table or some other way
        },
        error: function (xhr, status, error) {
            console.log(error);
        }
    });
}

function CheckGold(PoolSelection, times) {
    $.ajax({
        url: "/get_gold",
        type: "GET",
        success: function (user) {
            if (user.gold >= SINGLE_GACHA_PRICE[PoolSelection] * times) {
                //updateGold(userId, user.gold - amount);
                CallGacha(PoolSelection, times)
            } else {
                alert("没有足够的金币哦");
            }
        },
        error: function (xhr, status, error) {
            console.log(error);
        }
    });
}

// update gold value to backend
function UpdateGold(userId, amount) {
    $.ajax({
        url: "/update_gold",
        type: "POST",
        data: { user_id: userId, amount: amount },
        success: function (data) {
            // Success! Update the gold amount on the page
            UpdateGoldWebPage(data.gold);
        },
        error: function (xhr, status, error) {
            // Something went wrong...
            console.log("Error updating gold:", status, error);
        },
    });
}

function UpdateGoldWebPage(amount) {
    $('.user-gold').text(amount);
}

// function to update luck value to backend
function UpdateLuck(userId, luck) {
    $.ajax({
        url: "/update_luck",
        type: "POST",
        data: {user_id:userId, luck: luck },
        success: function (data) {
            // Success! Update the luck amount on the page
            const userLuckEl = document.getElementById("user-luck");
            userLuckEl.textContent = data;
        },
        error: function (xhr, status, error) {
            // Something went wrong...
            console.log("Error updating luck:", status, error);
        },
    });
}


function UpdateGachaTable() {
    // update gacha results
    var table = `<table class="table table-striped table-hover table-sm " id="gacha-result-table">`;
    table += "<thead><tr>";
    for (let item of HEADERS) {
        table += `<th class="header text-nowrap" scope="col">${item}</th>`;
    }
    table += "</tr></thead><tbody>";

    for (let batch of gachaResult) {
        for (let item of batch) {
            table += "<tr>";
            for (let info of KEYS) {
                table += `<td>${item[info]}</td>`
            }
            table += "</tr> ";
        }
    }
    table += "</tbody></table>";
    document.getElementById("main-table").innerHTML = table;
    $(document).ready(function () {
        $('#gacha-result-table').DataTable();
    });
}

// render inventory table
$(document).ready(function () {
    // get inventory items and populate them in the table
    var inventoryTable = $('#inventory').DataTable({
        ajax: {
            url: '/getinventory',
            dataSrc: 'inventory'
        },
        columns: [
            { data: 'equipment.name' },
            { data: 'equipment.rarity' },
            { data: 'equipment.class' },
            { data: 'equipment.stats' },
            { data: 'equipment.effect' },
            { data: 'timestamp' },
            {
                data: 'equipment_id',
                render: function (data, type, row) {
                    return '<button class="sell-btn" data-item-id="' + data + '">出售</button>';
                }
            }
        ]
        // TODO: 在表单上方增加信息栏，显示当前操作：卖掉了{name}，获得了{gold}
    });
    // handle click event for the sell button
    $('#inventory tbody').on('click', '.sell-btn', function (event) {
        // prevent the default action of the button, which is to submit the form
        event.preventDefault();
        var item_id = $(this).data('item-id');
        $.ajax({
            url: '/sell',
            type: 'POST',
            data: { 'equipment_id': item_id },
            success: function (data) {
                // update the inventory table
                inventoryTable.ajax.reload(null, false);
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });
});

$(document).ready(function () {
    // get inventory items and populate them in the table
    var inventoryTable = $('#inventory-all').DataTable({
        ajax: {
            url: '/getinventoryall',
            dataSrc: 'inventory'
        },
        columns: [
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
                    // add the user_id to the button's data attributes
                    return '<button class="sell-btn" data-item-id="' + data.equipment_id + '" data-target-id="' + data.user_id + '">移除</button>';
                }
            }
        ]
    });
    // handle click event for the sell button
    $('#inventory-all tbody').on('click', '.sell-btn', function (event) {
        // prevent the default action of the button, which is to submit the form
        event.preventDefault();
        var item_id = $(this).data('item-id');
        var target_id = $(this).data('target-id');
        $.ajax({
            url: '/remove',
            type: 'POST',
            data: { 'equipment_id': item_id, 'target_id': target_id },
            success: function (data) {
                // update the inventory table
                inventoryTable.ajax.reload(null, false);
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });
    // TODO: 删除后，撤销当前操作的悬浮窗，或者按钮
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
                    return '<button class="sell-btn" data-item-id="' + data.id + '">移除</button>';
                }
            }
        ]
    });

    // handle click event for the sell button
    $('#items-all tbody').on('click', '.sell-btn', function (event) {
        // prevent the default action of the button, which is to submit the form
        event.preventDefault();
        var item_id = $(this).data('item-id');
        $.ajax({
            url: '/remove',
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


// admin control for adding new equipment
function submitForm() {
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

$(document).ready(function () {
    $("#submit-btn").click(function (event) {
        submitForm();
    });
});

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

// function to add selected equipment to selected user
function addEquipmentToUser(userId, equipmentId) {
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
    });
}

$(document).ready(function () {
    // populate dropdowns
    populateDropdowns();
    // handle add equipment button click
    $('#add-equipment-btn').on('click', function (event) {
        var userId = $('#user-select').val();
        var equipmentId = $('#equipment-select option:selected').val(); // use .data() to get the equipment id
        addEquipmentToUser(userId, equipmentId);
    });
});

$(document).ready(function () {
    // handle update gold button click
    $('#update-gold-btn').on('click', function (event) {
        var userId = $('#user-select').val();
        var goldAmount = $('#gold-input').val();
        UpdateGold(userId, goldAmount);
    });
});

$(document).ready(function () {
    // handle update luck button click
    $('#update-luck-btn').on('click', function (event) {
        var userId = $('#user-select').val();
        var luckAmount = $('#luck-input').val();
        UpdateLuck(userId, luckAmount);
    });
});

function DownloadExcel() {
    //TODO: check database for available data
}
function ExportExcel(data) {
    filename = 'reports.xlsx';
    var ws = XLSX.utils.json_to_sheet(data);
    var wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
    XLSX.writeFile(wb, filename);
}

//nav menu transform
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function () {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if (currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });
})
