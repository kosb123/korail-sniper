var Common = {
	//기본 알림창
    bsAlert : function(type,msg,icon,timer,title,oBtnTitle,cBtnUse,cBtnTitle,okFn,cFn){
    	Swal.fire({
    		toast : type == 'm'?true:false,
			icon: typeof(icon) == 'undefined'?'info':icon,
			title: title,
			html: msg,
			timer : timer,
			showCancelButton:cBtnUse,
			confirmButtonColor:'#572b4c',
			confirmButtonText: typeof(oBtnTitle) == 'undefined'?'Ok':oBtnTitle,
			cancelButtonColor:'#666',
			cancelButtonText:typeof(cBtnTitle) == 'undefined'?'Cancel':cBtnTitle,
			allowOutsideClick:false,
			customClass:'swal-wide swal-txtL'
		}).then(function(result){
			if(result.isConfirmed && typeof(okFn) != 'undefined'){
				okFn();
			}else if(!result.isConfirmed && typeof(cFn) != 'undefined'){
				cFn();
			}
		});
    },	
	// 새창띄우기
	openWin : function (url, wname, width, height, scrl) {
		var winl = (screen.width - width) / 2;
		var wint = (screen.height - height) / 2;
		
		if (typeof scrl == "undefined") {
			var scroll = "no";
		} else {
			var scroll = scrl;
		}
		
		return window.open(url, wname, "left=" + winl + ", top=" + wint + ", scrollbars=" + scroll + ", status=no, resizable=no, width=" + width + ", height=" + height);
	},
	
	// 이메일 체크
	isAvailableEmail : function (v) {
		var format = /^((\w|[\-\.])+)@((\w|[\-\.])+)\.([A-Za-z]+)$/;
		
		if (v.search(format) == -1) {
			return false;
		} else if (v.charAt(v.indexOf('@') + 1) == '.') {
			return false;
		} else {
			return true;
		}
	},
	
	// 세자리마다 콤마찍기
	formatNumber : function (n) {
		var num = new String(n).replace(/\-/gi, "").replace(/,/gi, "").replace(/\./gi, "");
		var sgn = parseInt(num) < 0 || new String(n).substr(0, 1) == "-" ? "-" : "";
		var len = num.length;
		var pos = 3;
		var tmp = "";
		
		if (isNaN(num)) {
			window.alert("Only number it will be able to input.");
			return '0';
		} else if (parseInt(num) == 0) {
			return num;
		}
		
		while (len > 0) {
			len -= pos;
			
			if (len < 0) {
				pos = len + pos;
				len = 0;
			}
			
			tmp = "," + num.substr(len, pos) + tmp;
		}
		
		return sgn + tmp.substr(1);
	},
	
	// 문자열 길이
	strLen : function (str) {
		var len = 0;
		var tmp = null;
		var i = 0;
		
		while (i < str.length) {
			tmp = str.charAt(i);
			
			if (escape(tmp).length > 4) {
				len += 2;
			} else if (tmp != "\r") {
				len++;
			}
			
			i++;
		}
		
		return len;
	},
	
	// 문자열 자르기
	strCut : function (str, len, tail) {
		if (len == 0 || this.strLen(str) <= len) {
			return str;
		}
		
		var t = null;
		var i = 0;
		var l = 0;
		var returnValue = "";
		
		while (i < str.length) {
			t = str.charAt(i);

			if (escape(t).length > 4) {
				l += 2;
			} else if (t != "\r") {
				l += 1;
			}
			
			returnValue += t;
			
			if (l >= len) {
				break;
			}
			
			i++;
		}
		
		return returnValue + (typeof tail == "undefined" ? "..." : tail);
	},
	
	// 배열안에 값이 있는지 체크
	inArray : function (val, arr) {
		for (var i = 0; i < arr.length; i++) {
			if (arr[i] == val) {
				return true;
			}
		}
		
		return false;
	},
	
	// 라디오버튼 체크 여부
	radio : function (frm, act, val) {
		switch (act) {
			case 1 : // 체크값 구하기
				if (frm.length > 0) {
					for (var i = 0; i < frm.length; i++) {
						if (frm[i].checked == true) {
							return frm[i].value;
						}
					}
				} else {
					if (frm.checked == true) {
						return frm.value;
					}
				}
				
				break;
			case 2 : // 해당 위치에 포커스
				if (frm.length > 0) {
					for (var i = 0; i < frm.length; i++) {
						if (frm[i].value == val) {
							frm[i].checked = true;
							break;
						}
					}
				} else {
					if (frm.value == val) {
						frm.checked = true;
					}
				}
				
				break;
			case 3 : // 체크된 박스의 순번
				if (frm.length > 0) {
					for (var i = 0; i < frm.length; i++) {
						if (frm[i].value == val) {
							return i;
						}
					}
				} else {
					return 0;
				}
				
				break;
			case 4 : // 체크 해제
				if (frm.length > 0) {
					for (var i = 0; i < frm.length; i++) {
						frm[i].checked = false;
					}
				} else {
					frm.checked = false;
				}
				
				break;
			default : // 체크여부
				if (frm.length > 0) {
					for (var i = 0; i < frm.length; i++) {
						if (frm[i].checked == true) {
							return true;
						}
					}
				} else {
					if (frm.checked == true) {
						return true;
					}
				}
		}
		
		return false;
	},
	
	// 소숫점 자릿수 맞추기
	round : function (num, pos) {
		var posV = Math.pow(10, (pos >= 0 ? pos : 2));
		
		return Math.round(num * posV) / posV;
	},
	
	// 문자열 반복체크
	isRepetition : function (str, lmt) {
		for (var i = 0; i < str.length; i++) {
			var rpt = str.substr(i, 1);
			var key = '';
			
			for (var j = 0; j < lmt; j++) {
				key += rpt;
			}
			
			var chk = str.indexOf(key);
			
			if (chk >= 0) {
				return true;
			}
		}
		
		return false;
	},
	
	// 쿠키값 제어
	cookie : function (name, value, expire) {
		if (typeof value != 'undefined') {
			var day = new Date();
			day.setDate(day.getDate() + expire);
			document.cookie = name + "=" + escape(value) + "; path=/; expires=" + day.toGMTString() + ";";
		} else {
			var org = document.cookie;
			var dlm = name + "=";
			var x = 0;
			var y = 0;
			var z = 0;
			
			while (x <= org.length) {
				y = x + dlm.length;
				
				if (org.substring(x, y) == dlm) {
					if ((z = org.indexOf(";", y)) == -1) {
						z = org.length;
					}
					
					return org.substring(y, z);
				}
				
				x = org.indexOf(" ", x) + 1;
				
				if (x == 0) {
					break;
				}
			}
			
			return "";
		}
	},

	// 날짜목록 (년)
	yyList : function (y, s, e) {
		day = new Date();
		
		if (typeof y == "undefined") {
			var yy = day.getFullYear();
		} else if (y == "") {
			var yy = 0;
		} else {
			var yy = parseInt(y);
		}
		
		for (var i = (e ? e : day.getFullYear()); i >= (s ? s : 2013); i--) {
			document.write("<option value='" + i + "'" + (i == yy ? " selected" : "") + ">" + i + "</option>");
		}
	},
	
	// 날짜목록 (월)
	mmList : function (m) {
		day = new Date();
		
		if (typeof m == "undefined") {
			var mm = day.getMonth() + 1;
		} else if (m == "") {
			var mm = 0;
		} else {
			var mm = (m.substr(0, 1) == "0") ? parseInt(m.substr(1, m.length)) : parseInt(m);
		}
		
		for (var i = 1; i <= 12; i++) {
			var n = (i < 10 ? "0" : "") + i;
			
			document.write("<option value='" + n + "'" + (i == mm ? " selected" : "") + ">" + n + "</option>");
		}
	},
	
	// 날짜목록 (일)
	ddList : function (y, m, d) {
		day = new Date();
		
		if (typeof y == "undefined") {
			var yy = day.getFullYear();
		} else if (y == "") {
			var yy = 0;
		} else {
			var yy = parseInt(y);
		}
		
		if (typeof m == "undefined") {
			var mm = day.getMonth() + 1;
		} else if (m == "") {
			var mm = 0;
		} else {
			var mm = (m.substr(0, 1) == "0") ? parseInt(m.substr(1, m.length)) : parseInt(m);
		}
		
		if (typeof d == "undefined") {
			var dd = day.getDate();
		} else if (d == "") {
			var dd = 0;
		} else {
			var dd = (d.substr(0, 1) == "0") ? parseInt(d.substr(1, d.length)) : parseInt(d);
		}
		
		for (var i = 1; i <= this.endDate(yy, mm); i++) {
			var n = (i < 10 ? "0" : "") + i;
			
			document.write("<option value='" + n + "'" + (i == dd ? " selected" : "") + ">" + n + "</option>");
		}
	},
	
	// 날짜목록 (시)
	hhList : function (h) {
		for (var i = 0; i <= 23; i++) {
			var n = (i < 10 ? "0" : "") + i;
			
			document.write("<option value='" + n + "'" + (n == h ? " selected" : "") + ">" + n + "</option>");
		}
	},
	
	// 날짜목록 (분)
	iiList : function (m) {
		for (var i = 0; i <= 59; i++) {
			var n = (i < 10 ? "0" : "") + i;
			
			document.write("<option value='" + n + "'" + (n == m ? " selected" : "") + ">" + n + "</option>");
		}
	},
	
	// 날짜목록 (초)
	ssList : function (s) {
		for (var i = 0; i <= 59; i++) {
			var n = (i < 10 ? "0" : "") + i;
			
			document.write("<option value='" + n + "'" + (n == s ? " selected" : "") + ">" + n + "</option>");
		}
	},
	
	// 오늘 날짜
	ymd : function () {
		day = new Date();
		
		return day.getFullYear() + (day.getMonth() < 9 ? "0" : "") + (day.getMonth() + 1) + (day.getDate() < 10 ? "0" : "") + day.getDate();
	},
	
	// 윤년 여부
	isLeapYear : function (y) {
		if ((y % 4 == 0 && y % 100 != 0) || (y % 400 == 0 && y % 4000 != 0)) {
			return true;
		} else {
			return false;
		}
	},
	
	// 해당 월의 마지막 날짜
	endDate : function (y, m) {
		var edate = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
		
		if (m == 2) {
			if (this.isLeapYear(y) == true) {
				return 29;
			} else {
				return 28;
			}
		} else {
			return edate[m];
		}
	},
	
	// 목록 바꾸기
	changeDate : function (sel, y, m) {
		if (typeof y == "undefined" && typeof m == "undefined") {
			for (var i = 1; i <= 12; i++) {
				var n = (i < 10 ? "0" : "") + i;
				
				sel.options[i] = new Option(n, n);
			}
		} else {
			var ed = this.endDate(parseInt(y), (m.substr(0, 1) == "0") ? parseInt(m.substr(1, m.length)) : parseInt(m));
			
			for (var i = sel.length - 1; i > 0; i--) {
				sel.options[i] = null;
			}
			
			for (var i = 1; i <= ed; i++) {
				var n = (i < 10 ? "0" : "") + i;
				
				sel.options[i] = new Option(n, n);
			}
		}
	},
	
	isDate : function (sDate) {
		if (!/^[0-9]{8}$/.test(sDate)) {
			return false;
		}
		
		var y = parseInt(sDate.substr(0, 4));
		var m = parseInt(sDate.substr(4, 1) == '0' ? sDate.substr(5, 1) : sDate.substr(4, 2));
		var d = parseInt(sDate.substr(6, 1) == '0' ? sDate.substr(7, 1) : sDate.substr(6, 2));
		
		if (y < 0 || m <= 0 || d <= 0 || m > 12 || d > 31) {
			return false;
		} else if (d > this.endDate(y, m)) {
			return false;
		}
		
		return true;
	},
	
	// 좌/우 공백제거
	trim : function (str) {
		return str.replace(/(^\s*)|(\s*$)/gi, "");
	},
	
	// 배열 섞기
	shuffle : function (arr) {
		var tmp = [];
		
		for (var i = 0; i < arr.length; i++) {
			tmp[i] = arr[i];
		}
		
		tmp.sort ( function() { return Math.random() * 2 - 1; } );
		
		return tmp;
	},
	
	// 페이지 사이즈
	getPageSize : function () {
		var x, y, w, h;
		
		if (window.innerHeight && window.scrollMaxY) {
			x = window.innerWidth + window.scrollMaxX;
			y = window.innerHeight + window.scrollMaxY;
		} else if (document.body.scrollHeight > document.body.offsetHeight) {
			x = document.body.scrollWidth;
			y = document.body.scrollHeight;
		} else {
			x = document.body.offsetWidth;
			y = document.body.offsetHeight;
		}
		
		if (self.innerHeight) {
			if (document.documentElement.clientWidth){
				w = document.documentElement.clientWidth;
			} else {
				w = self.innerWidth;
			}
			h = self.innerHeight;
		} else if (document.documentElement && document.documentElement.clientHeight) {
			w = document.documentElement.clientWidth;
			h = document.documentElement.clientHeight;
		} else if (document.body) {
			w = document.body.clientWidth;
			h = document.body.clientHeight;
		}
		
		return {"width" : x < w ? x : w, "height" : y < h ? h : y};
	},
	
	// 스크롤 사이즈
	getScrollSize : function (obj) {
		var T, L, W, H;
		
		with (obj.document) {
			if (obj.document.documentElement && obj.document.documentElement.scrollTop) {
				T = obj.document.documentElement.scrollTop;
				L = obj.document.documentElement.scrollLeft;
			} else if (obj.document.body) {
				T = obj.document.body.scrollTop;
				L = obj.document.body.scrollLeft;
			}
			
			if (obj.innerWidth) {
				W = obj.innerWidth;
				H = obj.innerHeight;
			} else if (obj.document.documentElement && obj.document.documentElement.clientWidth) {
				W = obj.document.documentElement.clientWidth;
				H = obj.document.documentElement.clientHeight;
			} else {
				W = obj.document.body.offsetWidth;
				H = obj.document.body.offsetHeight
			}
		}
		
		return {"top" : T, "left" : L, "width" : W, "height" : H};
	},
	
	// 주민등록번호 체크
	isJuminNo : function (no) {
		var tot = 0;
		var add = '234567892345';
		
		if (!/^\d{6}[12340]\d{6}$/.test(no)) {
			return false;
		}
		
		for (var i = 0; i < 12; i++) {
			tot = tot + parseInt(no.substr(i, 1)) * parseInt(add.substr(i, 1));
		}
		
		tot = 11 - (tot % 11);
		
		if (tot == 10) {
			tot = 0;
		} else if (tot == 11) {
			tot = 1;
		}
		
		if (parseInt(no.substr(12, 1)) != tot) {
			return false;
		}
		
		return true;
	},
	
	// 외국인등록번호 체크
	isFgnNo : function (no) {
		var sum = 0;
		var odd = 0;
		var buf = new Array(13);
		
		if (!/^\d{6}[6789]\d{6}$/.test(no)) {
			return false;
		}
		
		for (var i = 0; i < 13; i++) {
			buf[i] = parseInt(no.charAt(i));
		}
		
		odd = buf[7] * 10 + buf[8];
		
		if(odd % 2 != 0) {
			return false;
		}
		
		var multipliers = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5];
		
		for(var i = 0; i < 12; i++) {
			sum += (buf[i] *= multipliers[i]);
		}
		
		sum = 11 - (sum%11);
		
		if(sum >= 10) {
			sum -= 10;
		}
		
		sum += 2;
		
		if(sum >= 10) {
			sum -= 10;
		}
		
		if (sum != buf[12]) {
			return false;
		}
		
		return true;
	},
	
	// 사업자등록번호 체크
	isBizNo : function (no) { 
		var check = new Array(1, 3, 7, 1, 3, 7, 1, 3, 5, 1);
		var sum = 0;
		var c2;
		var bizNo = no.replace(/-/gi, '');
		var remander;
		
		for (var i = 0; i <= 7; i++) {
			sum += check[i] * bizNo.charAt(i); 
		}
		
		c2 = "0" + (check[8] * bizNo.charAt(8)); 
		c2 = c2.substring(c2.length - 2, c2.length); 
		sum += Math.floor(c2.charAt(0)) + Math.floor(c2.charAt(1)); 
		
		if (Math.floor(bizNo.charAt(9)) == (10 - (sum % 10)) % 10) {
			return true;
		}
		
		return false; 
	},
	
	// 파일
	getFileSize : function (o) {
		if (o.files) {
			return o.files[0].size;
		}
		
		return new ActiveXObject("Scripting.FileSystemObject").getFile(o.value).size;
	},
	
	// 폼 체크
	checkForm : function (o) {
		var obj = o ? o : $$('body')[0];
		var returnValue = '';
		
		try {
			obj.getElementsBySelector('.checkForm').findAll(function (s) {
				if (returnValue != '') {
					return;
				} else if (s.disabled) {
					return;
				} else if (!s.getAttribute('option')) {
					return;
				}
				
				var v = Object.toJSON($H(eval('(' + s.getAttribute('option') + ')'))).evalJSON();
				
				if (v.sort) {
					v.message = v.sort + '번째 ' + v.message;
				}
				
				switch (s.tagName.toLowerCase()) {
					case 'input' :
						switch (s.type.toLowerCase()) {
							case 'file' :
								if (v.isMust && s.value == '') {
									returnValue = v.message;
								} else if (s.value != '') {
									if (v.limit) {
										var check = v.limit * 1024 * 1024;
										
										if (s.files) {
											if (s.getAttribute('multiple')) {
												for (var i = 0; i < s.files.length; i++) {
													if (s.files[i].size > check) {
														returnValue = (i + 1) + '번째 선택된 파일을 확인하십시오.\n\n세부내용 : 첨부파일은 ' + v.limit + 'MB까지만 업로드가 가능합니다.';
														break;
													}
												}
											} else {
												if (s.files[0].size > check) {
													returnValue = v.message.replace('첨부하십시오', '확인하십시오') + '\n\n세부내용 : 첨부파일은 ' + v.limit + 'MB까지만 업로드가 가능합니다.';
												}
											}
										}
									}
									
									if (v.limitExtension && v.limitExtension != '' && s.value != '' && returnValue == '') {
										if (v.limitExtension.indexOf(s.value.substr(s.value.lastIndexOf('.') + 1, s.value.length).toLowerCase()) >= 0) {
											returnValue = v.message.replace('첨부하십시오', '확인하십시오') + '\n\n세부내용 : 확장자가 ' + v.limitExtension + '인 파일은 업로드가 불가능합니다.';
										}
									} else if (v.allowExtension && v.allowExtension != '' && s.value != '' && returnValue == '') {
										if (v.allowExtension.indexOf(s.value.substr(s.value.lastIndexOf('.') + 1, s.value.length).toLowerCase()) < 0) {
											returnValue = v.message.replace('첨부하십시오', '확인십시오') + '\n\n세부내용 : 확장자가 ' + v.allowExtension + '인 파일만 업로드가 가능합니다.';
										}
									}
									
									//20210225 이동규 파일명 길이제한
									var fileValue = s.value.split('\\');
									var fileName = fileValue[fileValue.length-1];	//파일명
									var fileLength = fileName.length;
									if(v.textLimit < fileLength){
										returnValue = '파일명 저장 가능길이를 초과(현재 파일길이 : '+fileName.length+')했습니다.\n파일명('+v.textLimit+'자이하)을 변경 후 다시 저장해주세요';
									}
									
								}
								
								break;
							case 'radio' :
								if (v.isMust && !this.radio(document.getElementsByName(s.name))) {
									returnValue = v.message;
								}
								
								break;
							case 'checkbox' :
								if (v.isMust && !s.checked) {
									returnValue = v.message;
								}
								
								break;
							default :
								if (v.isMust && s.value == '') {
									returnValue = v.message;
								} else if (s.value != '') {
									v.message = v.message.replace('입력하십시오', '확인하십시오');
									
									if (s.getAttribute('maxlength') && parseInt(s.getAttribute('maxlength')) != s.value.length && v.equalLength) {
										switch (v.varType) {
											case 'date' :
												returnValue = v.message + '\n\n세부내용 : 해당 값이 년월일 ' + s.getAttribute('maxlength') + '자리가 맞는지 확인하십시오.';
												break;
											default :
												returnValue = v.message + '\n\n세부내용 : 해당 값이 ' + s.getAttribute('maxlength') + '자리가 맞는지 확인하십시오.';
										}
									} else if (s.getAttribute('maxlength') && parseInt(s.getAttribute('maxlength')) < s.value.length && !v.equalLength) {
										returnValue = v.message + '\n\n세부내용 : 해당 값이 ' + s.getAttribute('maxlength') + '자 이하인지 확인하십시오.';
									} else if (s.getAttribute('minlength') && parseInt(s.getAttribute('minlength')) > s.value.length && !v.equalLength) {
										returnValue = v.message + '\n\n세부내용 : 해당 값이 ' + s.getAttribute('minlength') + '자 이상인지 확인하십시오.';
									} else {
										switch (v.varType) {
											case 'number' :
												if (!/^[0-9]+$/.test(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 숫자만 입력이 가능합니다.';
												}
												
												break;
											case 'numberFormat' : 
												if (/[\s]/g.test(s.value) == true) {
													returnValue = v.message + '\n\n세부내용 : '+ (v.field) +' 입력시 공백은 사용할 수 없습니다.';
													break;
												} else if (!/^[0-9]+$/.test(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 숫자만 입력이 가능합니다.';
													break;
												} else {
													break;
												}
											case 'float' :
												if (!/^[0-9\.]+$/.test(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 숫자만 입력이 가능합니다.';
												}
												
												break;
											case 'alpha' :
												if (!/^[a-zA-Z]+$/.test(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 영문만 입력이 가능합니다.';
												}
												
												break;
											case 'alnum' :
												if (!/^[a-zA-Z0-9]+$/i.test(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 영문 및 숫자만 입력이 가능합니다.';
												}
												
												break;
											case 'alnum:a-z' :
												if (!/^[a-z0-9]+$/.test(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 영(소)문 및 숫자만 입력이 가능합니다.';
												}
												
												break;
											case 'alnum:A-Z' :
												if (!/^[A-Z0-9]+$/.test(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 영(대)문 및 숫자만 입력이 가능합니다.';
												}
												
												break;
											case 'url' :
												if (!/(http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/.test(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 유효하지 않은 URL입니다.';
												}
												
												break;
											case 'telNo' :
												if (!/^(0(2|3[1-3]|4[1-4]|5[1-5]|6[1-4])|070)-?[0-9]{3,4}-?[0-9]{4}$/.test(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 유효하지 않은 일반전화번호입니다.';
												}
												
												break;
											case 'telNoFormat' :
												if (/[\s]/g.test(s.value) == true) {
													returnValue = v.message + '\n\n세부내용 : '+ (v.field) +' 입력시 공백은 사용할 수 없습니다.';
													break;
												} else if (!/^(0(2|3[1-3]|4[1-4]|5[1-5]|6[1-4])|070)-?[0-9]{3,4}-?[0-9]{4}$/.test(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 유효하지 않은 일반전화번호입니다.';
													break;
												} else {
													break;
												}
											case 'celNo' :
												if (!/^(01[016789]{1}|050)-?[0-9]{3,4}-?[0-9]{4}$/.test(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 유효하지 않은 휴대전화번호입니다.';
												}
												
												break;
											case 'celNoFormat' :
												if (/[\s]/g.test(s.value) == true) {
													returnValue = v.message + '\n\n세부내용 : '+ (v.field) +' 입력시 공백은 사용할 수 없습니다.';
													break;
												} else if (!/^(01[016789]{1}|050)-?[0-9]{3,4}-?[0-9]{4}$/.test(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 유효하지 않은 휴대전화번호입니다.';
													break;
												} else {
													break;
												}
											case 'email' :
												if (!/^((\w|[\-\.])+)@((\w|[\-\.])+)\.([A-Za-z]+)$/.test(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 잘못된 이메일 형식입니다.';
												}
												
												break;
											case 'emailFormat' :
												if (/[\s]/g.test(s.value) == true) {
													returnValue = v.message + '\n\n세부내용 : '+ (v.field) +' 입력시 공백은 사용할 수 없습니다.';
													break;
												} else if (!/^((\w|[\-\.])+)@((\w|[\-\.])+)\.([A-Za-z]+)$/.test(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 잘못된 이메일 형식입니다.';
													break;
												} else {
													break;
												}
											case 'id' :
												if (!/^[a-z0-9]{2,12}$/.test(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 2자 이상 12자 이하의 영(소)문과 숫자의 조합만 사용가능합니다.';
												}
												
												break;
											case 'password' :
												if (s.value.length < 8 || s.value.length > 16) {
													returnValue = v.message + '\n\n세부내용 : 8자 이상 16자 이하로 입력하십시오.';
												} else if (s.value.search(/\s/) != -1) {
													returnValue = v.message + '\n\n세부내용 : 공백없이 입력하십시오.';
												} else if ( s.value.search(/[\'\"<>;\-+=\/\\]/gi) > 0) {
													returnValue = v.message + '\n\n"\'"(작은 따옴표), """(큰 따옴표), "<"(부등호 작음), ">"(부등호 큼), ";"(쌍반점), "-"(빼기), "+"(더하기), "="(같음), "/"(사선), "\\"(역사선)를 제외한 특수문자를 사용해주세요';
												} else if (s.value.search(/[0-9]/gi) < 0 || s.value.search(/[a-z]/gi) < 0  || s.value.search(/['~!@#$%^&*()_\[\]{}\|:\?]/) < 0) {
													//660098 패스워드 특수문자 추가
													returnValue = v.message + '\n\n세부내용 : 영문, 숫자, 특수문자를 혼합하여 입력하십시오.';
												}
												else if (this.isRepetition(s.value, 4)) {
													returnValue = v.message + '\n\n세부내용 : 같은 문자를 4번 이상 반복할 수 없습니다.';
												}
												
												break;
											case 'date' :
											case 'date-only-past' :
											case 'date-only-future' :
												if (!this.isDate(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 유효하지 않은 날짜입니다.';
												} else if (v.varType == 'date-only-past' && parseInt(s.value) > parseInt(this.ymd())) {
													returnValue = v.message + '\n\n세부내용 : 오늘보다 미래입니다.';
												} else if (v.varType == 'date-only-future' && parseInt(s.value) < parseInt(this.ymd())) {
													returnValue = v.message + '\n\n세부내용 : 오늘보다 과거입니다.';
												}
												
												break;
											case 'juminNo' :
												if (!this.isJuminNo(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 유효하지 않은 주민등록번호입니다.';
												}
												
												break;
											case 'fgnNo' :
												if (!this.isFgnNo(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 유효하지 않은 외국인등록번호입니다.';
												}
												
												break;
											case 'bizNo' :
												if (!this.isBizNo(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 유효하지 않은 사업자등록번호입니다.';
												}
												
												break;
											case 'amount' :
												if (!/^[0-9\,]+$/.test(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 유효하지 않은 금액입니다.';
												}
												
												break;
											case 'isHanEng' :
												if (!/^[a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣]+$/.test(s.value)) {
													returnValue = v.message + '\n\n세부내용 : 한글 또는 영문만 입력 가능합니다.';
												}
												
												break;
										}
									}
								}
						}
						
						break;
					case 'select' :
						if (v.isMust && s.options.selectedIndex == 0) {
							returnValue = v.message;
						}
						
						break;
					case 'textarea' :
						if (v.isMust && s.value == '') {
							returnValue = v.message;
						} else if (s.value) {
							if (s.getAttribute('maxlength') && parseInt(s.getAttribute('maxlength')) < s.value.length) {
								returnValue = v.message + '\n\n세부내용 : 해당 값이 ' + s.getAttribute('maxlength') + '자 이하인지 확인하십시오.';
							}
						}
						
						break;
				}
				
				if (returnValue == '' && v.equalValue) {
					var check = $(v.equalValue);
					
					if (s.value != check.value) {
						returnValue = v.message + '\n\n세부내용 : 해당 값이 일치하지 않습니다.';
					}
				}
				
				if (returnValue == '' && v.isMustWhenIsNotEmptyValue) {
					var check = $(v.isMustWhenIsNotEmptyValue);
					
					if (check.value != '' && s.value == '') {
						returnValue = v.message;
					}
				}
				
				if (returnValue == '' && v.isMustWhenIsTrueObject) {
					var check = eval(v.isMustWhenIsTrueObject);
					
					if (check) {
						switch (s.tagName.toLowerCase()) {
							case 'input' :
								switch (s.type.toLowerCase()) {
									case 'radio' :
										if (!this.radio(document.getElementsByName(s.name))) {
											returnValue = v.message;
										}
										
										break;
									case 'checkbox' :
										if (!s.checked) {
											returnValue = v.message;
										}
										
										break;
									default :
										if (s.value == '') {
											returnValue = v.message;
										}
								}
								
								break;
							case 'select' :
								if (s.selectedIndex == 0) {
									returnValue = v.message;
								}
								
								break;
							case 'textarea' :
								if (s.value == '') {
									returnValue = v.message;
								}
								
								break;
						}
					}
				}
				
				if (returnValue == '' && v.isLessThan) {
					var check = $(v.isLessThan);
					
					if (check && check.value != '' && s.value != '' && parseFloat(check.value) <= parseFloat(s.value)) {
						returnValue = v.message.replace('입력하십시오', '확인하십시오').replace('선택하십시오', '확인하십시오') + '\n\n세부내용 : ' + v.confirmMessage;
					}
				}
				
				if (returnValue == '' && v.isLessEqual) {
					var check = $(v.isLessEqual);
					
					if (check && check.value != '' && s.value != '' && parseFloat(check.value) < parseFloat(s.value)) {
						returnValue = v.message.replace('입력하십시오', '확인하십시오').replace('선택하십시오', '확인하십시오') + '\n\n세부내용 : ' + v.confirmMessage;
					}
				}
				
				if (returnValue == '' && v.isGreaterThan) {
					var check = $(v.isGreaterThan);
					
					if (check && check.value != '' && s.value != '' && parseFloat(check.value) >= parseFloat(s.value)) {
						returnValue = v.message.replace('입력하십시오', '확인하십시오').replace('선택하십시오', '확인하십시오') + '\n\n세부내용 : ' + v.confirmMessage;
					}
				}
				
				if (returnValue == '' && v.isGreaterEqual) {
					var check = $(v.isGreaterEqual);
					
					if (check && check.value != '' && s.value != '' && parseFloat(check.value) > parseFloat(s.value)) {
						returnValue = v.message.replace('입력하십시오', '확인하십시오').replace('선택하십시오', '확인하십시오') + '\n\n세부내용 : ' + v.confirmMessage;
					}
				}
				
				if (returnValue != '') {
					try {
						var scrl = this.getScrollSize(window);
						
						if ($(s).cumulativeOffset()[1] < scrl.top + 70) {
							Effect.ScrollTo(s, {duration : 0, offset : -300, afterFinish : function () { (v.focus ? $(v.focus) : s).focus(); }.bind(this)});
						} else {
							s.focus();
						}
					} catch (e) {}
				}
			}.bind(this));
		} catch (e) {
			returnValue = e.message;
		}
		
		return returnValue;
	},
	
	// 이미지 사이즈 보정
	adjustImageLength : function (ow, oh, mw, mh) {
		var as = [mw, mh];
		var rw, rh;
		
		if (mw > 0 && mh > 0) {
			if (ow > mw || oh > mh) {
				rw = ow / mw;
				rh = oh / mh;
				
				if (rw > rh) {
					as[0] = mw;
					as[1] = Math.ceil(oh * mw / ow);
				} else {
					as[0] = Math.ceil(ow * mh / oh);
					as[1] = mh;
				}
			} else {
				as[0] = ow;
				as[1] = oh;
			}
		} else if (mw > 0) {
			if (ow > mw) {
				as[0] = mw;
				rw = mw / ow;
			} else {
				as[0] = ow;
				rw = 1;
			}
			
			as[1] = Math.ceil(oh * rw);
		} else if (mh > 0) {
			if (oh > mh) {
				as[1] = mh;
				rh = mh / oh;
			} else {
				as[1] = oh;
				rh = 1;
			}
			
			as[0] = Math.ceil(ow * rh);
		}
		
		return as;
	},
	
	// 쿠키생성
	setCookie : function(name,value,expiredays){
    	var cookie = name + "=" +escape(value) + "; path=/;";
    	if(typeof expiredays != 'undefined'){
    		var todayDate = new Date();
    		todayDate.setDate(todayDate.getDate()+expiredays);
    		cookie += "expires=" + todayDate.toGMTString() + ";";
    	}
    	document.cookie = cookie;
    },
    
    // 쿠키제거
    getCookie : function(name) {
        var nameOfCookie = name + "=";
        var x = 0;

        while (x <= document.cookie.length) {
                var y = x + nameOfCookie.length;
                if (document.cookie.substring(x, y) == nameOfCookie) {
                        if ((endOfCookie = document.cookie.indexOf( ";", y )) == -1) {
                                endOfCookie = document.cookie.length;
                        }
                        return unescape(document.cookie.substring(y, endOfCookie));
                }
                x = document.cookie.indexOf(" ", x) + 1;
                if (x == 0) {
                        break;
                }
        }
    },
	
    //쿠키삭제
    deleteCookie : function(name){
    	setCookie(name,"",-1);
    },
    
	// 날짜 더하기
	addDay : function (n) {
		var date = new Date();
		
		return new Date(date.getFullYear(), date.getMonth(), date.getDate() + n);
	},
	
	// 날짜 계산
	calDate : function (n) {
		var date = new Date();
		var s, e;
		
		switch (n) {
			case 1  : // 어제
				s = new Date(date.getFullYear(), date.getMonth(), date.getDate() - 1);
				e = s;
				break;
			case 2  : // 이번달
				s = new Date(date.getFullYear(), date.getMonth(), 1);
				e = new Date(date.getFullYear(), date.getMonth(), Common.endDate(date.getFullYear(), date.getMonth() + 1));
				break;
			case 3  : // 지난달
				s = new Date(date.getFullYear(), date.getMonth() - 1, 1);
				e = new Date(date.getFullYear(), date.getMonth() - 1, Common.endDate(date.getFullYear(), date.getMonth()));
				break;
			case 4  : // 다음달
				s = new Date(date.getFullYear(), date.getMonth() + 1, 1);
				e = new Date(date.getFullYear(), date.getMonth() + 1, Common.endDate(date.getFullYear(), date.getMonth() + 2));
				break;
			case 5  : // 이번주
			case 6  : // 지난주
			case 7  : // 다음주
				var w = (new Date()).getDay() - 1;
				
				if (w == -1) {
					w = 6;
				}
				
				switch (n) {
					case 5 :
						s = this.addDay(w * -1);
						e = this.addDay(w * -1 + 6);
						break;
					case 6 :
						s = this.addDay(w * -1 - 7);
						e = this.addDay(w * -1 - 1);
						break;
					case 7 :
						s = this.addDay(w * -1 + 7);
						e = this.addDay(w * -1 + 13);
						break;
				}
				
				break;
			case 8  : // 올해
				s = new Date(date.getFullYear(), 0, 1);
				e = new Date(date.getFullYear(), 11, 31);
				break;
			case 9  : // 작년
				s = new Date(date.getFullYear() - 1, 0, 1);
				e = new Date(date.getFullYear() - 1, 11, 31);
				break;
			default : // 오늘
				s = date;
				e = date;
				break;
		}
		
		return {"s" : s, "e" : e};
	}
};

// equals java.net.URLEncoder.encode(str, "UTF-8")
function encodeURIComponentEx(str) {
	var returnValue = "";
	var s, u;
	
	for (var i = 0; i < str.length; i++) {
		s = str.charAt(i);
		u = str.charCodeAt(i);
		
		if (s == " ") {
			returnValue += "+";
		} else {
			if (u == 0x2a || u == 0x2d || u == 0x2e || u == 0x5f || ((u >= 0x30) && (u <= 0x39)) || ((u >= 0x41) && (u <= 0x5a)) || ((u >= 0x61) && (u <= 0x7a))) {
				returnValue += s;
			} else {
				if ((u >= 0x0) && (u <= 0x7f)) {
					s = "0" + u.toString(16);
					returnValue += "%" + s.substr(s.length - 2);
				} else if (u > 0x1fffff) {
					returnValue += "%" + (oxf0 + ((u & 0x1c0000) >> 18)).toString(16);
					returnValue += "%" + (0x80 + ((u & 0x3f000) >> 12)).toString(16);
					returnValue += "%" + (0x80 + ((u & 0xfc0) >> 6)).toString(16);
					returnValue += "%" + (0x80 + (u & 0x3f)).toString(16);
				} else if (u > 0x7ff) {
					returnValue += "%" + (0xe0 + ((u & 0xf000) >> 12)).toString(16);
					returnValue += "%" + (0x80 + ((u & 0xfc0) >> 6)).toString(16);
					returnValue += "%" + (0x80 + (u & 0x3f)).toString(16);
				} else {
					returnValue += "%" + (0xc0 + ((u & 0x7c0) >> 6)).toString(16);
					returnValue += "%" + (0x80 + (u & 0x3f)).toString(16);
				}
			}
		}
	}
	
	return returnValue;
}

// equals java.net.URLDecoder.decode(str, "UTF-8")
function decodeURIComponentEx(str) {
	var returnValue = "";
	var s, u, n, f;
	
	for (var i = 0; i < str.length; i++) {
		s = str.charAt(i);
		
		if (s == "+") {
			returnValue += " ";
		} else {
			if (s != "%") {
				returnValue += s;
			} else {
				u = 0;
				f = 1;
				
				while (true) {
					var ss = "";
					
					for (var j = 0; j < 2; j++) {
						var sss = str.charAt(++i);
						
						if (((sss >= "0") && (sss <= "9")) || ((sss >= "a") && (sss <= "f"))  || ((sss >= "A") && (sss <= "F"))) {
							ss += sss;
						} else {
							--i;
							break;
						}
					}
					
					n = parseInt(ss, 16);
					
					if (n <= 0x7f) { u = n; f = 1; }
					if (n >= 0xc0 && n <= 0xdf) { u = n & 0x1f; f = 2; }
					if (n >= 0xe0 && n <= 0xef) { u = n & 0x0f; f = 3; }
					if (n >= 0xf0 && n <= 0xf7) { u = n & 0x07; f = 4; }
					if (n >= 0x80 && n <= 0xbf) { u = (u << 6) + (n & 0x3f); --f; }
					
					if (f <= 1) {
						break;
					}
					
					if (str.charAt(i + 1) == "%") {
						i++;
					} else {
						break;
					}
				}
				
				returnValue += String.fromCharCode(u);
			}
		}
	}
	
	return returnValue;
}

function isEng(obj)
{
    var strWord = obj.value;
    var res = "";

    for (var i = 0; i < strWord.length; i++){
    	var temp = strWord.substring(i, i+1);
    	if (/^[a-zA-Z]+$/.test(temp)) {
    		res = res + temp;
    	}
    }
    obj.value = res;
}

function isNum(obj)
{
    var strWord = obj.value;
    var res = "";

    for (var i = 0; i < strWord.length; i++){
    	var temp = strWord.substring(i, i+1);
    	if (/^[0-9]+$/.test(temp)) {
    		res = res + temp;
    	}
    }
    obj.value = res;
}

function isHanEng(obj)
{
    var strWord = obj.value;
    var res = "";

    for (var i = 0; i < strWord.length; i++){
    	var temp = strWord.substring(i, i+1);
    	if (/^[a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣]+$/.test(temp)) {
    		res = res + temp;
    	}
    }
    obj.value = res;
}

function isPassword(id, printId){
	var resValue = '';
	var input = $J('input[id="'+id+'"]');
	var print = $J('#'+printId);
	if(input.length <= 0) {
		return null;
	}
	if(input.val() == ''){
		resValue = '';
		print.css("display", "none");
	} else if (input.val().length < 8 || input.val().length > 16) {
		//resValue = '8자 이상 16자 이하로 입력하십시오.';
		resValue = '비밀번호가 적절하지 않습니다.';
		print.css("display", "block");
		print.css("color", "#9c1737");
	} else if (input.val().search(/\s/) != -1) {
		//resValue = '세부내용 : 공백없이 입력하십시오.';
		resValue = '비밀번호가 적절하지 않습니다.';
		print.css("color", "#9c1737");
		print.css("display", "block");
	} else if (input.val().search(/[\'\"<>;\-+=\/\\]/gi) > 0) {
		//resValue = '"\'"(작은 따옴표), """(큰 따옴표), "<"(부등호 작음), ">"(부등호 큼), ";"(쌍반점), "-"(빼기), "+"(더하기), "="(같음), "/"(사선), "\\"(역사선)를 제외한 특수문자를 사용해주세요';
		resValue = '비밀번호가 적절하지 않습니다.';
		print.css("color", "#9c1737");
		print.css("display", "block");
	} else if (input.val().search(/[0-9]/gi) < 0 || input.val().search(/[a-z]/gi) < 0 || input.val().search(/[~!@#$%^&*()]/gi) < 0) {
		//resValue = '영문, 숫자, 특수문자를 혼합하여 입력하십시오.';
		resValue = '비밀번호가 적절하지 않습니다.';
		print.css("color", "#9c1737");
		print.css("display", "block");
	} else if (Common.isRepetition(input.val(), 4)) {
		//resValue= '같은 문자를 4번 이상 반복할 수 없습니다.';
		resValue = '비밀번호가 적절하지 않습니다.';
		print.css("color", "#9c1737");
		print.css("display", "block");
	} else {
		resValue = '비밀번호가 적절합니다.';
		print.css("color", "#58bd63");
		print.css("display", "block");
	}
	print.html(resValue);
}
