;

/**
 * City instance
 */
class City {
    /**
     * The district and districtValue must have the same length
     * @param name: The name of city
     * @param district: Key
     * @param districtValue: Value
     * @constructor
     */
    constructor(name, district, districtValue) {
        this.name = name;
        this.district = district;
        this.district.push('unlimited');
        this.districtValue = districtValue;
        this.districtValue.push('unlimited');
        this.kw = {};
        this.init();
    }

    init() {
        if (this.district.length === this.districtValue.length)
            for (let index = 0; index < this.district.length; index++)
                this.kw[this.district[index]] = this.districtValue[index];
        else
            console.log('A error happended in the constructure of the City.');
    }
}

let shanghai = new City('shanghai', ['baoshan district', 'changning district', 'chongming district', 'fengxian district', 'hongkou district', 'huangpu district',
    'jiading district', 'jingan district', 'jinshan district', 'minhang district', 'pudong district', 'putuo district', 'qingpu district', 'songjiang district', 'xuhui district',
    'yangpu district'], ['baoshan', 'changning', 'chongming', 'fengxian', 'hongkou', 'huangpu',
    'jiading', 'jingan', 'jinshan', 'minhang', 'pudong', 'putuo', 'qingpu', 'songjiang', 'xuhui',
    'yangpu']);
let container = [shanghai,];
let kwContainer = {};

/**
 * Strategy
 * This class is a interface and process elements changing
 */
class DefaultStrategy {
    /**
     * @param city: a instance of City
     * @param target: the select object
     */
    process(city, target) {
        target.options.length = 0;  //remove the initial element
        for (let index = 0; index < city.district.length; index++) {
            let key = city.district[index];
            let value = city.kw[key];
            target.add(new Option(key, value));
        }
    }
}

let strategy = new DefaultStrategy();

/**
 * For change and display the price
 */
function priceChange() {
    let target = document.getElementById('value');
    let value = document.getElementById('formControlRange').value;

    target.innerText = value !== '700' ? 'Max price: ' + value : 'Unlimited';
}

/**
 * For submit the data of html table to the web server
 */
function submit() {
    let city = $('#inlineFormCustomSelect1');
    let district = $('#inlineFormCustomSelect2');
    let maxPrice = $('#formControlRange');
    let dateBegin = $('#dateBegin');
    let dateEnd = $('#dateEnd');
    let btn = $('#btn');

    $.ajax('./submit', {
        data: {
            area: city.val(),
            location: district.val(),
            maxPrice: maxPrice.val(),
            dateBegin: dateBegin.val(),
            dateEnd: dateEnd.val()
        },
        type: 'get',
        dataType: 'json',
        complete: function () {
            btn.removeClass('disabled');
        },
        success: function (info, code, _) {
             if (code === 'success')
                 window.location.href = window.location.href + '/result/' + info.key;
        },
        error: function (_) {
            console.log('A error happended in the process of submitting.');
        },
        beforeSend: function () {
            btn.addClass('disabled');
        }
    })
}

/**
 * For check the integrality of html table
 */
function check() {
    let city = $('#inlineFormCustomSelect1');
    let dateBegin = $('#dateBegin');
    let dateEnd = $('#dateEnd');

    return city.val() !== 'none' && dateBegin.val() && dateEnd.val();
}

/**
 * For changed the datetime range
 */
function setMinimumDate(target) {
    let date = new Date();
    let month = date.getMonth() + 1;
    let day = date.getDate();

    if (month <= 9 && month >= 1)
        month = '0' + month;
    if (day <= 9 && day >= 1)
        day = '0' + day;

    let today = date.getFullYear() + '-' + month + '-' + day;
    target.setAttribute('min', today);
}

/**
 * Handler
 */
function submitHandler() {
    let btn = $('#btn');

    if (!btn.hasClass('disabled') && check())
        submit();
    else if (btn.hasClass('disabled'))
        layer.msg('Please wait for a minute.', {
            offset: 't',
            anim: 6
        });
    else
        layer.msg('Please fill all information.', {
            offset: 't',
            anim: 6
        });

}

function dateChangeHandler() {
    let end = document.getElementById('dateEnd');
    let begin = $('#dateBegin');
    let date = new Date(begin.val());  // get today
    let month = date.getMonth() + 1;
    let day = date.getDate() + 1;

    if (month <= 9 && month >= 1)
        month = '0' + month;
    if (day <= 9 && day >= 1)
        day = '0' + day;

    end.setAttribute('min', date.getFullYear() + '-' + month + '-' + day);
}

function cityChangeHandler() {
    let district = document.getElementById('inlineFormCustomSelect2');
    let curCity = $('#inlineFormCustomSelect1');

    if (curCity.val() !== 'none') {
        let cityObj = kwContainer[curCity.val()];  // get city obj
        strategy.process(cityObj, district);
    } else {
        district.options.length = 0;
        district.add(new Option('Please choose a city', 'none'));
    }
}

function priceChangeHandler() {
    priceChange();
}

/**
 * Initial
 */
jQuery(function () {
    let selectTarget = document.getElementById('inlineFormCustomSelect1');

    for (let index = 0; index < container.length; index++)
        selectTarget.add(new Option(container[index].name, container[index].name));  // add city option

    setMinimumDate(document.getElementById('dateBegin'));  // set minimum datetime
    setMinimumDate(document.getElementById('dateEnd'));

    for (let index = 0; index < container.length; index++)
        kwContainer[container[index].name] = container[index];  // construct a dict
});
